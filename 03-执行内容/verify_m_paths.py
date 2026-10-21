from pathlib import Path
import json
p=Path(r'C:\Users\sunny\Documents\MSIT Northwestern\projects\project-0011-Chicago311-PowerBI\05-交付物\powerbi')
m=json.loads((p/'Operations.SemanticModel/model.bim').read_text(encoding='utf-8'))
for t in m['model']['tables']:
 expr='\n'.join(t['partitions'][0]['source']['expression'])
 assert '\\u' not in expr,expr
 assert (p.parents[1]/'03-执行内容/data'/(t['name']+'.csv')).exists()
# A separate entry point forces Desktop to reload externally corrected source.
a=json.loads((p/'Chicago311.pbip').read_text(encoding='utf-8'));(p/'Chicago311-Validated.pbip').write_text(json.dumps(a,indent=2),encoding='utf-8')
print('Five M file paths verified; reload entry created')

