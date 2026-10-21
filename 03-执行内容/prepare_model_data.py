from pathlib import Path
import pandas as pd,numpy as np,json,sqlite3,datetime,hashlib
p=Path(__file__).resolve().parents[1]; raw=p/'01-需求与原始资料'; out=p/'03-执行内容/data';out.mkdir(exist_ok=True)
m=json.loads((raw/'source-manifest.json').read_text());a=[]
for f in m['pages']:a+=json.loads((raw/f['file']).read_text())
d=pd.DataFrame(a);n0=len(d);d=d.sort_values('last_modified_date').drop_duplicates('sr_number',keep='last').copy()
for c in ['created_date','closed_date','last_modified_date']:d[c]=pd.to_datetime(d[c],errors='coerce')
asof=pd.Timestamp(m['completed_utc']).tz_convert('America/Chicago').tz_localize(None)
for c in ['duplicate','legacy_record']:d[c]=d[c].fillna(False).astype(bool)
status=d.status.value_counts().to_dict();print('statuses',status)
d['status_closed']=d.status.isin(['Completed','Closed'])
d['valid_closed']=d.status_closed & d.closed_date.notna() & (d.closed_date>=d.created_date) & (d.closed_date<=asof)
d['is_included']=~d.duplicate & ~d.legacy_record & d.created_date.notna()
d['is_open']=d.status.eq('Open')
d['is_canceled']=d.status.eq('Canceled')
assert set(d.status.unique()) <= {'Completed','Closed','Open','Canceled'}
# Closed with a missing/invalid date stays closed, excluded only from duration measures.
d['resolution_days']=((d.closed_date-d.created_date).dt.total_seconds()/86400).where(d.valid_closed)
d['open_age_days']=((asof-d.created_date).dt.total_seconds()/86400).where(d.is_open)
d['created_day']=d.created_date.dt.strftime('%Y-%m-%d');d['closed_day']=d.closed_date.dt.strftime('%Y-%m-%d')
d['created_month']=d.created_date.dt.strftime('%Y-%m');d['created_week']= (d.created_date.dt.normalize()-pd.to_timedelta(d.created_date.dt.dayofweek,unit='D')).dt.strftime('%Y-%m-%d')
d['community_area']=pd.to_numeric(d.community_area,errors='coerce').fillna(0).astype(int);d['ward']=pd.to_numeric(d.ward,errors='coerce').fillna(0).astype(int)
d['age_band']=pd.cut(d.open_age_days,bins=[-np.inf,7,30,90,np.inf],labels=['0–7 days','8–30 days','31–90 days','Over 90 days']).astype('string').fillna('Closed')
d['service_type']=d.sr_type.map({'Graffiti Removal Request':'Graffiti removal','Pothole in Street Complaint':'Street potholes','Street Light Out Complaint':'Street light outages'})
keep=['sr_number','service_type','status','created_day','closed_day','created_month','created_week','community_area','ward','duplicate','legacy_record','is_included','status_closed','valid_closed','is_open','is_canceled','resolution_days','open_age_days','age_band','origin','owner_department']
f=d[keep].copy();f.to_csv(out/'FactRequests.csv',index=False)
types=pd.DataFrame({'service_type':sorted(f.service_type.unique())});types.to_csv(out/'DimService.csv',index=False)
areas=pd.DataFrame({'community_area':sorted(f.community_area.unique())});areas['area_label']=areas.community_area.map(lambda x:'Unknown' if x==0 else f'Community area {x:02}');areas.to_csv(out/'DimArea.csv',index=False)
dates=pd.DataFrame({'Date':pd.date_range('2025-10-01',asof.normalize())});dates['Month']=dates.Date.dt.strftime('%Y-%m');dates['Week']=(dates.Date-pd.to_timedelta(dates.Date.dt.dayofweek,unit='D')).dt.strftime('%Y-%m-%d');dates['Date']=dates.Date.dt.strftime('%Y-%m-%d');dates.to_csv(out/'DimCreatedDate.csv',index=False);dates.to_csv(out/'DimClosedDate.csv',index=False)
# SQLite runs the SQL transformations; CSVs are portable import snapshots for Power Query.
con=sqlite3.connect(out/'operations.sqlite');f.to_sql('requests',con,if_exists='replace',index=False)
sql="""WITH eligible AS (SELECT * FROM requests WHERE is_included=1), by_month AS (SELECT created_month,COUNT(*) requests,SUM(status_closed) closed,SUM(is_open) open FROM eligible GROUP BY created_month) SELECT *, requests-LAG(requests) OVER (ORDER BY created_month) AS month_change FROM by_month ORDER BY created_month;"""
(p/'03-执行内容/monthly_operations.sql').write_text(sql,encoding='utf-8');pd.read_sql_query(sql,con).to_csv(out/'monthly_operations.csv',index=False)
sql2="""SELECT service_type,COUNT(*) AS requests,SUM(status_closed) AS closed,SUM(is_open) AS open,AVG(CASE WHEN valid_closed=1 THEN resolution_days END) AS mean_valid_closed_days FROM requests WHERE is_included=1 GROUP BY service_type ORDER BY open DESC;"""
(p/'03-执行内容/service_operations.sql').write_text(sql2,encoding='utf-8');s=pd.read_sql_query(sql2,con);s.to_csv(out/'service_operations.csv',index=False)
e=f[f.is_included];closed=e[e.valid_closed];op=e[e.is_open]
summary={'raw_rows':n0,'unique_requests':len(f),'duplicate_ids_removed':n0-len(f),'source_duplicate_flag':int(f.duplicate.sum()),'legacy_flag':int(f.legacy_record.sum()),'included_requests':len(e),'closed_requests':int(e.status_closed.sum()),'canceled_requests':int(e.is_canceled.sum()),'open_cohort_requests':int(e.is_open.sum()),'valid_closed_duration':len(closed),'closed_invalid_or_missing_date':int((e.status_closed & ~e.valid_closed).sum()),'median_closed_days':float(closed.resolution_days.median()),'p90_closed_days':float(closed.resolution_days.quantile(.9)),'median_open_age_days':float(op.open_age_days.median()),'asof_local':str(asof),'source_statuses':status,'services':s.to_dict('records')}
checks={'unique_request_ids':bool(f.sr_number.is_unique),'cohort_partition':len(e)==summary['closed_requests']+summary['open_cohort_requests']+summary['canceled_requests'],'sql_total_equals_pandas':int(s.requests.sum())==len(e),'sql_open_equals_pandas':int(s.open.sum())==len(op),'duration_nonnegative':bool((closed.resolution_days>=0).all()),'no_unmapped_service':bool(f.service_type.notna().all()),'date_dim_covers_fact':bool(set(f.created_day.dropna())<=set(dates.Date))}
assert all(checks.values()),checks
(p/'04-验证与测试/data-validation.json').write_text(json.dumps({'checks':checks,'summary':summary},indent=2),encoding='utf-8')
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
# A deterministic 300-row review sample for later Excel formula checks, not a full-data Excel claim.
f.sample(min(300,len(f)),random_state=20261020).to_csv(out/'excel_review_sample.csv',index=False)
print(json.dumps(summary,indent=2))

