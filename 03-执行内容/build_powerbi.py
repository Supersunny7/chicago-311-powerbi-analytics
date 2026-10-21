from pathlib import Path
import json,uuid,shutil,ast
import pandas as pd
p=Path(__file__).resolve().parents[1];data=p/'03-执行内容/data';dest=p/'05-交付物/powerbi';dest.mkdir(exist_ok=True)
report=dest/'Operations.Report';model=dest/'Operations.SemanticModel';definition=report/'definition';definition.mkdir(parents=True,exist_ok=True)
seed=Path(r'C:\Users\sunny\Documents\MSIT Northwestern\projects\project-0007-Ecommerce-Analytics\99-临时与缓存\pbi-seed.Report')
summary=json.loads((data/'summary.json').read_text())
def dump(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
measures={
'Requests':('CALCULATE(COUNTROWS(FactRequests), FactRequests[is_included] = TRUE())','#,0'),
'Closed Requests':('CALCULATE([Requests], FactRequests[status_closed] = TRUE())','#,0'),
'Open Cohort Requests':('CALCULATE([Requests], FactRequests[is_open] = TRUE())','#,0'),
'Closed Share':('DIVIDE([Closed Requests], [Requests])','0.0%'),
'Valid Closed Requests':('CALCULATE([Requests], FactRequests[valid_closed] = TRUE())','#,0'),
'Median Closed Days':('CALCULATE(MEDIAN(FactRequests[resolution_days]), FactRequests[is_included] = TRUE(), FactRequests[valid_closed] = TRUE())','0.0'),
'P90 Closed Days':('PERCENTILEX.INC(FILTER(FactRequests, FactRequests[is_included] && FactRequests[valid_closed]), FactRequests[resolution_days], 0.9)','0.0'),
'Median Open Age Days':('CALCULATE(MEDIAN(FactRequests[open_age_days]), FactRequests[is_included] = TRUE(), FactRequests[is_open] = TRUE())','0.0'),
'Open Over 90 Days':('CALCULATE([Open Cohort Requests], FactRequests[open_age_days] > 90)','#,0'),
'Open Over 90 Share':('DIVIDE([Open Over 90 Days], [Open Cohort Requests])','0.0%'),
'Invalid Closed Dates':('CALCULATE([Closed Requests], FactRequests[valid_closed] = FALSE())','#,0')}
tables=[]
for name in ['FactRequests','DimService','DimArea','DimCreatedDate','DimClosedDate']:
 f=pd.read_csv(data/(name+'.csv'));cols=[];types=[]
 for c in f.columns:
  typ='boolean' if c in ['duplicate','legacy_record','is_included','status_closed','valid_closed','is_open','is_canceled'] else 'dateTime' if c in ['created_day','closed_day','Date'] else 'int64' if c in ['community_area','ward'] else 'double' if c in ['resolution_days','open_age_days'] else 'string'
  col={'name':c,'dataType':typ,'sourceColumn':c,'summarizeBy':'none'}
  if typ=='dateTime':col['formatString']='yyyy-MM-dd'
  if name=='FactRequests' and c in ['duplicate','legacy_record','is_included','status_closed','valid_closed','is_open','sr_number']:col['isHidden']=True
  cols.append(col);mt={'boolean':'type logical','dateTime':'type date','int64':'Int64.Type','double':'type number','string':'type text'}[typ];types.append('{'+json.dumps(c)+', '+mt+'}')
 path=(data/(name+'.csv')).as_posix()
 m='let\n Source = Csv.Document(File.Contents('+json.dumps(path,ensure_ascii=False)+'), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),\n Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n Typed = Table.TransformColumnTypes(Headers, {'+', '.join(types)+'}, "en-US")\nin\n Typed'
 t={'name':name,'columns':cols,'partitions':[{'name':name,'mode':'import','source':{'type':'m','expression':m.splitlines()}}]}
 if name=='FactRequests':t['measures']=[{'name':n,'expression':e,'formatString':fmt,'displayFolder':'Service operations'} for n,(e,fmt) in measures.items()]
 tables.append(t)
rels=[]
for fc,tt,tc in [('service_type','DimService','service_type'),('community_area','DimArea','community_area'),('created_day','DimCreatedDate','Date'),('closed_day','DimClosedDate','Date')]:rels.append({'name':str(uuid.uuid4()),'fromTable':'FactRequests','fromColumn':fc,'toTable':tt,'toColumn':tc,'fromCardinality':'many','toCardinality':'one','crossFilteringBehavior':'oneDirection','isActive':True})
dump(model/'definition.pbism',{'version':'4.2','settings':{}})
dump(model/'model.bim',{'name':'Operations','compatibilityLevel':1606,'model':{'culture':'en-US','defaultPowerBIDataSourceVersion':'powerBI_V3','sourceQueryCulture':'en-US','tables':tables,'relationships':rels,'annotations':[{'name':'__PBI_TimeIntelligenceEnabled','value':'0'}]}})
dump(dest/'Chicago311.pbip',{'version':'1.0','artifacts':[{'report':{'path':'Operations.Report'}}],'settings':{'enableAutoRecovery':True}})
dump(report/'definition.pbir',{'version':'4.0','datasetReference':{'byPath':{'path':'../Operations.SemanticModel'}}})
shutil.copytree(seed/'StaticResources',report/'StaticResources',dirs_exist_ok=True)
for f in ['report.json','version.json']:shutil.copyfile(seed/'definition'/f,definition/f)
def literal(v):return {'expr':{'Literal':{'Value':('true' if v else 'false') if isinstance(v,bool) else str(v)+'D' if isinstance(v,(int,float)) else "'"+str(v).replace("'","''")+"'"}}}
def color(v):return {'solid':{'color':literal(v)}}
def field(table,col,measure=False):return {('Measure' if measure else 'Column'):{'Expression':{'SourceRef':{'Entity':table}},'Property':col}}
def proj(t,c,m=False):return {'field':field(t,c,m),'queryRef':t+'.'+c,'nativeQueryRef':c,'displayName':c.replace('_',' ').title()}
def visual(page,name,kind,x,y,w,h,roles=None,title=None,objects=None,sort=None):
 v={'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json','name':name,'position':{'x':x,'y':y,'z':1,'height':h,'width':w,'tabOrder':1},'visual':{'visualType':kind,'drillFilterOtherVisuals':True}}
 vc={'background':[{'properties':{'show':literal(True),'color':color('#FFFFFF'),'transparency':literal(0)}}],'border':[{'properties':{'show':literal(False)}}]}
 if title:vc['title']=[{'properties':{'show':literal(True),'text':literal(title),'fontColor':color('#173E43'),'fontSize':literal(12),'bold':literal(True),'fontFamily':literal('Segoe UI')}}]
 v['visual']['visualContainerObjects']=vc
 if roles:v['visual']['query']={'queryState':{r:{'projections':[proj(*f) for f in fs]} for r,fs in roles.items()}}
 if sort:v['visual']['query']['sortDefinition']={'sort':[{'field':field(*sort[:3]),'direction':sort[3]}],'isDefaultSort':False}
 if objects:v['visual']['objects']=objects
 dump(definition/'pages'/page/'visuals'/name/'visual.json',v);return v

def text(page,name,value,x,y,w,h,size=13,fg='#173E43',bg='#EFF5F5'):
 v=visual(page,name,'textbox',x,y,w,h,objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':value,'textStyle':{'fontFamily':'Segoe UI','fontSize':str(size)+'pt','color':fg}}]}]}}]})
 v['visual']['visualContainerObjects']['background'][0]['properties']['color']=color(bg);dump(definition/'pages'/page/'visuals'/name/'visual.json',v)

def card(page,n,label,x,y):
 visual(page,n.replace(' ','_'),'card',x,y,304,105,{'Values':[('FactRequests',n,True)]},label,{'labels':[{'properties':{'color':color('#173E43'),'fontSize':literal(30),'labelDisplayUnits':literal(0),'labelPrecision':literal(1 if measures[n][1]!='#,0' else 0)}}],'categoryLabels':[{'properties':{'show':literal(False)}}]})
chartobj={'categoryAxis':[{'properties':{'fontSize':literal(10),'fontFamily':literal('Segoe UI')}}],'valueAxis':[{'properties':{'fontSize':literal(10)}}],'dataPoint':[{'properties':{'defaultColor':color('#277D80')}}],'legend':[{'properties':{'fontSize':literal(10),'position':literal('Top')}}]}
def chart(page,name,kind,x,y,w,h,cat,values,title,chron=False):
 visual(page,name,kind,x,y,w,h,{'Category':[(cat[0],cat[1],False)],'Y':[('FactRequests',n,True) for n in values]},title,chartobj,sort=(cat[0],cat[1],False,'Ascending') if chron else ('FactRequests',values[0],True,'Descending'))
pages=[('overview','Operations overview'),('performance','Closure performance'),('backlog','Cohort backlog')]
dump(definition/'pages/pages.json',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json','pageOrder':[p for p,_ in pages],'activePageName':'overview'})
for pg,label in pages:
 dump(definition/'pages'/pg/'page.json',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json','name':pg,'displayName':label,'displayOption':'FitToPage','height':800,'width':1320,'objects':{'background':[{'properties':{'color':color('#EFF5F5'),'transparency':literal(0)}}]}})
 text(pg,'title',label,28,18,850,48,size=25)
 text(pg,'subtitle','Chicago 311 | Requests created Oct 2025–Sep 2026 | Status snapshot '+summary['asof_local'][:10],30,68,1180,30,size=11,fg='#49676B')
 visual(pg,'type_slicer','slicer',1000,18,290,52,{'Values':[('DimService','service_type',False)]},'Service type',{'data':[{'properties':{'mode':literal('Dropdown')}}],'selection':[{'properties':{'singleSelect':literal(False),'selectAllCheckboxEnabled':literal(True)}}]})
 text(pg,'footer','Source: City of Chicago | Duplicates and legacy excluded | Closure is an administrative status, not verified resolution',30,766,1260,24,size=9,fg='#49676B')
for i,(n,label) in enumerate([('Requests','Included requests'),('Closed Share','Share currently closed'),('Open Cohort Requests','Still open in this cohort'),('Median Closed Days','Median days to close')]):card('overview',n,label,30+i*320,114)
chart('overview','arrivals','lineChart',30,244,770,290,('DimCreatedDate','Month'),['Requests'],'Monthly request arrivals',True)
chart('overview','type_mix','barChart',820,244,470,290,('DimService','service_type'),['Requests'],'Request volume by service')
text('overview','scope','Read this as a cohort study\n\nThis report follows three request types created in a fixed twelve-month window. Open counts describe the remaining requests in that cohort at extraction. They do not include older citywide carry-in backlog.',30,555,1260,180,size=15)
for i,(n,label) in enumerate([('Closed Requests','Currently closed'),('Valid Closed Requests','Valid closure durations'),('Median Closed Days','Median days to close'),('P90 Closed Days','90th percentile days to close')]):card('performance',n,label,30+i*320,114)
chart('performance','duration_type','clusteredBarChart',30,244,620,300,('DimService','service_type'),['Median Closed Days','P90 Closed Days'],'Closure duration by service type')
chart('performance','closures','lineChart',670,244,620,300,('DimClosedDate','Month'),['Closed Requests'],'Closures by month within this cohort',True)
visual('performance','area_table','tableEx',30,566,1260,170,{'Values':[('DimArea','area_label',False),('FactRequests','Requests',True),('FactRequests','Median Closed Days',True),('FactRequests','P90 Closed Days',True)]},'Community area comparison — compare within the same service type',sort=('FactRequests','Requests',True,'Descending'))
for i,(n,label) in enumerate([('Open Cohort Requests','Open in this cohort'),('Median Open Age Days','Median open age in days'),('Open Over 90 Days','Open for over 90 days'),('Open Over 90 Share','Share of open over 90 days')]):card('backlog',n,label,30+i*320,114)
chart('backlog','age_band','barChart',30,244,620,285,('FactRequests','age_band'),['Open Cohort Requests'],'Open request age distribution')
chart('backlog','open_type','barChart',670,244,620,285,('DimService','service_type'),['Open Cohort Requests'],'Open cohort requests by service type')
visual('backlog','priority_table','tableEx',30,551,1260,190,{'Values':[('DimArea','area_label',False),('FactRequests','Open Cohort Requests',True),('FactRequests','Open Over 90 Days',True),('FactRequests','Median Open Age Days',True)]},'Investigation shortlist — age is an analysis threshold, not an official SLA',sort=('FactRequests','Open Over 90 Days',True,'Descending'))
(dest/'DAX_measures.txt').write_text('\n\n'.join(n+' =\n'+e for n,(e,_) in measures.items()),encoding='utf-8')
dump(p/'04-验证与测试/powerbi-build.json',{'tables':5,'relationships':4,'measures':len(measures),'pages':3,'desktop_validation':'pending','pbix_saved':False})
print(dest/'Chicago311.pbip')


