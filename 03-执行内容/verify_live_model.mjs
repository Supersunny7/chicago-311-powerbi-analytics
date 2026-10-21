import {Client} from 'file:///C:/Users/sunny/.codex/tools/powerbi/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js';
import {StdioClientTransport} from 'file:///C:/Users/sunny/.codex/tools/powerbi/node_modules/@modelcontextprotocol/sdk/dist/esm/client/stdio.js';
import fs from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const c=new Client({name:'Chicago311-evidence',version:'1.0.0'});
const t=new StdioClientTransport({command:'C:/Users/sunny/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe',args:['C:/Users/sunny/.codex/tools/powerbi/node_modules/@microsoft/powerbi-modeling-mcp/index.js','--start'],stderr:'pipe'});
async function call(name,request){const r=await c.callTool({name,arguments:{request}},undefined,{timeout:120000});if(r.isError)throw Error(JSON.stringify(r));return JSON.parse(r.content.find(x=>x.type==='text').text);}
try{
 await c.connect(t);
 const instances=await call('connection_operations',{operation:'ListLocalInstances'});
 const found=instances.data.filter(x=>x.parentWindowTitle==='Chicago311');if(found.length!==1)throw Error('Expected exactly one Chicago311 instance');
 await call('connection_operations',{operation:'Connect',connectionString:found[0].connectionString});
 const query='EVALUATE ROW("raw_rows",COUNTROWS(FactRequests),"included_requests",[Requests],"closed_requests",[Closed Requests],"open_cohort_requests",[Open Cohort Requests],"canceled_requests",CALCULATE([Requests],FactRequests[is_canceled]=TRUE()),"closed_share",[Closed Share],"valid_closed_duration",[Valid Closed Requests],"median_closed_days",[Median Closed Days],"p90_closed_days",[P90 Closed Days],"median_open_age_days",[Median Open Age Days],"open_over_90",[Open Over 90 Days],"open_over_90_share",[Open Over 90 Share],"closed_invalid_or_missing_date",[Invalid Closed Dates])';
 const totals=await call('dax_query_operations',{operation:'Execute',query,resultMode:'Inline'});
 const services=await call('dax_query_operations',{operation:'Execute',query:'EVALUATE SUMMARIZECOLUMNS(DimService[service_type],"Requests",[Requests],"Closed",[Closed Requests],"Open",[Open Cohort Requests],"Median",[Median Closed Days],"P90",[P90 Closed Days]) ORDER BY DimService[service_type]',resultMode:'Inline'});
 const age=await call('dax_query_operations',{operation:'Execute',query:'EVALUATE SUMMARIZECOLUMNS(FactRequests[age_band],FactRequests[Age band order],"Open",[Open Cohort Requests]) ORDER BY FactRequests[Age band order]',resultMode:'Inline'});
 await fs.writeFile(path.join(root,'04-验证与测试/live-dax-results.json'),JSON.stringify({verifiedAt:new Date().toISOString(),connection:found[0].parentWindowTitle,query,totals,services,age},null,2));
 console.log(JSON.stringify({totals:totals.data.rows,services:services.data.rows,age:age.data.rows}));
}finally{await c.close();}
