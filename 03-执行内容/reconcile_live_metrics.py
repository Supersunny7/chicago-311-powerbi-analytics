from pathlib import Path
import json, math
import pandas as pd
p=Path(__file__).resolve().parents[1]
data=p/'03-执行内容/data'
live=json.loads((p/'04-验证与测试/live-dax-results.json').read_text(encoding='utf-8'))
df=pd.read_csv(data/'FactRequests.csv')
inc=df[df.is_included];closed=inc[inc.status_closed];valid=inc[inc.valid_closed];opened=inc[inc.is_open]
expected={'raw_rows':len(df),'included_requests':len(inc),'closed_requests':len(closed),'open_cohort_requests':len(opened),'canceled_requests':int(inc.is_canceled.sum()),'closed_share':len(closed)/len(inc),'valid_closed_duration':len(valid),'median_closed_days':valid.resolution_days.median(),'p90_closed_days':valid.resolution_days.quantile(.9),'median_open_age_days':opened.open_age_days.median(),'open_over_90':int((opened.open_age_days>90).sum()),'open_over_90_share':float((opened.open_age_days>90).mean()),'closed_invalid_or_missing_date':int((~closed.valid_closed).sum())}
actual={k.strip('[]'):v for k,v in live['totals']['data']['rows'][0].items()}
checks=[]
def check(name,a,e):
 ok=a is not None and math.isclose(float(a),float(e),rel_tol=1e-10,abs_tol=1e-8)
 checks.append({'metric':name,'power_bi':a,'python':float(e),'passed':ok})
for k,e in expected.items():check(k,actual[k],e)
for row in live['services']['data']['rows']:
 name=row['DimService[service_type]'];sub=inc[inc.service_type.eq(name)];v=sub[sub.valid_closed]
 for metric,e in {'Requests':len(sub),'Closed':sub.status_closed.sum(),'Open':sub.is_open.sum(),'Median':v.resolution_days.median(),'P90':v.resolution_days.quantile(.9)}.items():check(name+'/'+metric,row['['+metric+']'],e)
for row in live['age']['data']['rows']:
 label=row['FactRequests[age_band]'];check('Age/'+label,row['[Open]'],int(opened.age_band.eq(label).sum()))
assert expected['included_requests']==expected['closed_requests']+expected['open_cohort_requests']+expected['canceled_requests']
result={'verified_at':live['verifiedAt'],'checks':checks,'check_count':len(checks),'all_passed':all(c['passed'] for c in checks),'method':'Actual live MCP DAX results independently compared with CSV data in pandas; continuous linear P90; tolerance 1e-8 days.'}
(p/'04-验证与测试/live-metric-reconciliation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert result['all_passed'],result
print(f"PASS: {len(checks)} live Power BI / Python metric comparisons")
