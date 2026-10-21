import { Client } from 'file:///C:/Users/sunny/.codex/tools/powerbi/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js';
import { StdioClientTransport } from 'file:///C:/Users/sunny/.codex/tools/powerbi/node_modules/@modelcontextprotocol/sdk/dist/esm/client/stdio.js';
import fs from 'node:fs/promises';
import readline from 'node:readline';
const root='C:/Users/sunny/Documents/MSIT Northwestern/projects/project-0011-Chicago311-PowerBI';
const transport=new StdioClientTransport({command:'C:/Users/sunny/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe',args:['C:/Users/sunny/.codex/tools/powerbi/node_modules/@microsoft/powerbi-modeling-mcp/index.js','--start'],env:{...process.env,npm_config_cache:root+'/99-临时与缓存/npm-cache'},stderr:'pipe'});
const client=new Client({name:'Chicago311-validation',version:'1.0.0'});
transport.stderr?.on('data',b=>process.stderr.write(b));
await client.connect(transport);
const list=await client.listTools();
await fs.writeFile(root+'/04-验证与测试/mcp-tool-schemas.json',JSON.stringify(list,null,2));
console.log(JSON.stringify({ready:true,tools:list.tools.map(x=>({name:x.name,description:x.description.slice(0,180)}))}));
const lines=readline.createInterface({input:process.stdin,crlfDelay:Infinity});
for await(const line of lines){
 if(!line.trim())continue;
 try{const q=JSON.parse(line);if(q.exit){await client.close();break;}const result=await client.callTool({name:q.name,arguments:q.arguments||{}},undefined,{timeout:120000});console.log(JSON.stringify({result}));}
 catch(e){console.log(JSON.stringify({error:String(e)}));}
}
