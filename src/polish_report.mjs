import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const pages=path.join(root,'deliverables/powerbi/Operations.Report/definition/pages');
const lit=v=>({expr:{Literal:{Value:typeof v==='boolean'?String(v):typeof v==='number'?`${v}D`:`'${v.replaceAll("'","''")}'`}}});
const col=v=>({solid:{color:lit(v)}});
const props=(p,id)=>[{properties:p,...(id?{selector:{id:'default'}}:{})}];
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const write=(p,v)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(v,null,2));};
const colors={ink:'#142D3A',muted:'#536976',teal:'#176C70',amber:'#B56A24',canvas:'#F4F6F7',white:'#FFFFFF'};
const titles={overview:'01 / Service demand & outcomes',performance:'02 / Speed beyond the average',backlog:'03 / Where to investigate next'};
const notes={overview:'SCOPE / Three services · one fixed creation cohort\nRequests created Oct 2025–Sep 2026; status captured 20 Oct 2026. Duplicate and legacy flags are excluded. Canceled requests remain separate from open requests. Select a service to explore; clear it to return to all three.',performance:'READING THE DISTRIBUTION / Median describes a typical closed request; P90 exposes the slower tail. Compare community areas within the same service type. Closure is an administrative status, not resident-confirmed resolution.',backlog:'PRIORITIZATION / Start with older open requests, then inspect service type and community area. Over 90 days is an analysis threshold, not an official SLA. This cohort excludes requests created before Oct 2025.'};
for(const pg of ['overview','performance','backlog']){
 const base=path.join(pages,pg), pf=path.join(base,'page.json'), page=read(pf);
 page.displayOption='FitToPage';page.objects.background=props({color:col(colors.canvas),transparency:lit(0)});write(pf,page);
 const files=fs.readdirSync(path.join(base,'visuals')).map(n=>path.join(base,'visuals',n,'visual.json')).filter(fs.existsSync);
 const cards=[];
 for(const file of files){
  const v=read(file), n=v.name, vis=v.visual, p=v.position;
  if(vis.visualType==='card'){cards.push({file,v});continue;}
  if(vis.visualType==='textbox'){
   const run=vis.objects.general[0].properties.paragraphs[0].textRuns[0];
   run.textStyle.color=colors.ink;
   if(n==='title'){run.value=titles[pg];run.textStyle.fontSize='26pt';run.textStyle.fontWeight='bold';p.y=20;p.height=50;}
   if(n==='subtitle'){run.value='CHICAGO 311  /  Oct 2025–Sep 2026 cohort  /  Snapshot 20 Oct 2026';run.textStyle.fontSize='11pt';run.textStyle.color=colors.muted;}
   if(n==='scope'){run.value=notes[pg];run.textStyle.fontSize='13pt';p.y=600;p.height=132;}
   if(n==='footer'){run.value='CITY OF CHICAGO OPEN DATA  ·  Historical cohort study  ·  Administrative closure ≠ verified resolution';run.textStyle.fontSize='9pt';run.textStyle.color=colors.muted;}
   vis.visualContainerObjects.background=props({show:lit(true),color:col(colors.canvas),transparency:lit(0)});
  } else if(n==='type_slicer'){
   p.y=20;p.height=62;
  } else {
   vis.visualContainerObjects.title[0].properties.fontColor=col(colors.ink);
   vis.visualContainerObjects.title[0].properties.fontSize=lit(13);
   if(vis.objects?.dataPoint){
    vis.objects.categoryAxis=props({fontSize:lit(11),fontFamily:lit('Segoe UI')});
    vis.objects.valueAxis=props({fontSize:lit(10)});
    vis.objects.dataPoint=props({defaultColor:col(colors.teal)});
   }
   if(n==='duration_type')vis.objects.dataPoint=[{properties:{fill:col(colors.teal)},selector:{metadata:'FactRequests.Median Closed Days'}},{properties:{fill:col(colors.amber)},selector:{metadata:'FactRequests.P90 Closed Days'}}];
   if(n==='arrivals'||n==='type_mix'){p.y=286;p.height=290;}
   if(n==='duration_type'||n==='closures'){p.y=258;p.height=260;}
   if(n==='age_band'||n==='open_type'){p.y=258;p.height=260;}
   if(n==='age_band')vis.query.sortDefinition={sort:[{field:{Column:{Expression:{SourceRef:{Entity:'FactRequests'}},Property:'age_band'}},direction:'Ascending'}],isDefaultSort:false};
   if(n==='area_table'||n==='priority_table'){
    const all=vis.query.queryState.Values.projections;
    vis.visualType='pivotTable';vis.query.queryState={Rows:{projections:all.filter(x=>x.field.Column)},Values:{projections:all.filter(x=>x.field.Measure)}};
    p.y=540;p.height=166;
    vis.objects={columnHeaders:props({fontSize:lit(11),fontColor:col(colors.ink),columnAdjustment:lit('growToFit'),autoSizeColumnWidth:lit(true)}),rowHeaders:props({fontSize:lit(11),stepped:lit(false)}),values:props({fontSize:lit(11)})};
   }
  }
  write(file,v);
 }
 cards.sort((a,b)=>a.v.position.x-b.v.position.x);
 const first=structuredClone(cards[0].v), H=page.height, vf=Math.min(28,Math.max(12,Math.floor(H*.028))),lf=Math.min(14,Math.max(8,Math.floor(vf*.55))), ch=34+Math.ceil(vf*1.5)+Math.ceil(Math.max(lf,12)*1.5);
 first.name='headline_metrics';first.position={x:30,y:118,z:2,width:1260,height:ch,tabOrder:2};
 first.visual={visualType:'cardVisual',drillFilterOtherVisuals:true,query:{queryState:{Data:{projections:cards.map(({v})=>{const q=v.visual.query.queryState.Values.projections[0];q.displayName=v.visual.visualContainerObjects.title[0].properties.text.expr.Literal.Value.slice(1,-1);return q;})}}},objects:{
  value:props({fontSize:lit(vf),fontColor:col(colors.ink),bold:lit(true),labelDisplayUnits:lit('1')},true),
  label:props({fontSize:lit(lf),fontColor:col(colors.muted),position:lit('aboveValue')},true),
  outline:props({show:lit(false)},true),layout:props({style:lit('Table'),columnCount:lit(4),rowCount:lit(1),paddingUniform:lit(0),customizeLines:lit(true),gridlineWidth:lit(1),gridlineColor:col('#DFE6EA')},true),
  cardCalloutArea:props({show:lit(true),backgroundFillColor:col(colors.white),backgroundTransparency:lit(0),paddingUniform:lit(8)})
 },visualContainerObjects:{background:props({show:lit(true),color:col(colors.white),transparency:lit(0)}),border:props({show:lit(false)}),padding:props({top:lit(8),bottom:lit(8),left:lit(8),right:lit(8)},true)}};
 write(path.join(base,'visuals/headline_metrics/visual.json'),first);
 // Only remove the exact legacy files already backed up; leave all other visuals.
 for(const {file} of cards)fs.unlinkSync(file);
 const template=read(path.join(base,'visuals/subtitle/visual.json'));
 template.name='reading_note';template.position={x:30,y:218,z:3,width:1260,height:40,tabOrder:3};
 template.visual.objects.general[0].properties.paragraphs[0].textRuns[0]={value:pg==='overview'?'START HERE / Understand demand, then inspect the slower closure tail and the remaining open cohort.':pg==='performance'?'COMPARE / Teal = median days  ·  Amber = P90 days  ·  Filter to one service before comparing areas.':'FOCUS / Age bands are ordered from newest to oldest. The area list is ranked by open requests over 90 days.',textStyle:{fontFamily:'Segoe UI',fontSize:'12pt',color:colors.teal}};
 write(path.join(base,'visuals/reading_note/visual.json'),template);
 if(pg!=='overview'){
  const foot=read(path.join(base,'visuals/subtitle/visual.json'));foot.name='method_note';foot.position={x:30,y:714,z:3,width:1260,height:44,tabOrder:4};foot.visual.objects.general[0].properties.paragraphs[0].textRuns[0]={value:notes[pg],textStyle:{fontFamily:'Segoe UI',fontSize:'10pt',color:colors.muted}};write(path.join(base,'visuals/method_note/visual.json'),foot);
 }
}
console.log('Polished three pages; migrated headline cards and area matrices.');
