from pathlib import Path
import urllib.request,urllib.parse,json,time,datetime,hashlib
p=Path(__file__).resolve().parents[1]
TYPES=['Graffiti Removal Request','Pothole in Street Complaint','Street Light Out Complaint']
where="created_date >= '2025-10-01T00:00:00' AND created_date < '2026-10-01T00:00:00' AND sr_type in ("+','.join("'"+x+"'" for x in TYPES)+')'
fields='sr_number,sr_type,status,created_date,closed_date,last_modified_date,community_area,ward,duplicate,legacy_record,origin,owner_department'
raw=p/'01-需求与原始资料'; pages=[];offset=0; started=datetime.datetime.now(datetime.timezone.utc).isoformat()
while True:
 params={'$select':fields,'$where':where,'$order':'sr_number','$limit':50000,'$offset':offset}
 u='https://data.cityofchicago.org/resource/v6vf-nfxy.json?'+urllib.parse.urlencode(params)
 dest=raw/f'requests-{offset:06}.json'
 for attempt in range(3):
  try:
   b=urllib.request.urlopen(u,timeout=90).read();a=json.loads(b);break
  except Exception:
   if attempt==2:raise
   time.sleep(2)
 dest.write_bytes(b);pages.append({'file':dest.name,'rows':len(a),'sha256':hashlib.sha256(b).hexdigest(),'query_url':u})
 print('page',offset,len(a),flush=True)
 if len(a)<50000:break
 offset+=50000
manifest={'source':'City of Chicago 311 Service Requests','dataset_id':'v6vf-nfxy','landing_url':'https://data.cityofchicago.org/d/v6vf-nfxy','started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cohort_start':'2025-10-01','cohort_end_exclusive':'2026-10-01','types':TYPES,'pages':pages,'limitations':['Extraction is paged, not a transactionally frozen source snapshot.','Current status at extraction; no status-change history.','Cohort backlog excludes requests created outside the window.','Completed status does not establish resident-confirmed resolution.']}
(raw/'source-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('total',sum(x['rows'] for x in pages))
