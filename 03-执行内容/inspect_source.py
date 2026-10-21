from pathlib import Path
import urllib.request,urllib.parse,json,datetime
p=Path(r'C:\Users\sunny\Documents\MSIT Northwestern\projects\project-0011-Chicago311-PowerBI')
def get(q):
 url='https://data.cityofchicago.org/resource/v6vf-nfxy.json?'+urllib.parse.urlencode(q)
 return json.load(urllib.request.urlopen(url,timeout=60))
meta=json.load(urllib.request.urlopen('https://data.cityofchicago.org/api/views/v6vf-nfxy.json',timeout=60))
(p/'01-需求与原始资料/source-metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
print('COLUMNS',[(c['fieldName'],c['dataTypeName']) for c in meta['columns'] if not c['fieldName'].startswith(':')])
q={'$select':'sr_type,count(*) AS requests','$where':"created_date >= '2025-10-01T00:00:00' AND created_date < '2026-10-01T00:00:00'",'$group':'sr_type','$order':'requests DESC','$limit':30}
a=get(q);(p/'02-研究与笔记/type-profile.json').write_text(json.dumps(a,indent=2),encoding='utf-8');print('TYPES',json.dumps(a))
