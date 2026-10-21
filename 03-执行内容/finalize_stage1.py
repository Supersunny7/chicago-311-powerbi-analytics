from pathlib import Path
from pypdf import PdfReader
from docx import Document
import json
r=Path(r'C:\Users\sunny\Documents\MSIT Northwestern');p=r/'projects/project-0007-Ecommerce-Analytics'
f=p/'05-交付物/Sunny_Li_Resume_2026_Data_Analyst_Dated.docx';d=Document(f)
assert any('Olist E-commerce Analytics\tOct 2026' in x.text for x in d.paragraphs)
pdf=p/'04-验证与测试/resume-dated/Sunny_Li_Resume_2026_Data_Analyst_Dated.pdf';assert len(PdfReader(str(pdf)).pages)==1
with (p/'00-项目管理/执行记录.md').open('a',encoding='utf-8') as h:h.write('\n2026-10-20：简历Olist项目日期补为Oct 2026，技术栈移至链接行；按10-11创建/10-13分析/10-19网页/10-20公开交付记录，不使用数据年份代替制作日期。原件保留，本地另存05-交付物/Sunny_Li_Resume_2026_Data_Analyst_Dated.docx。一页渲染及日期文本验证通过，Dashboard已有Jan2017–Aug2018历史范围无需修改。Power BI新项目登记为0011。\n')
p2=r/'projects/project-0011-Chicago311-PowerBI'
with (p2/'项目说明.md').open('a',encoding='utf-8') as h:h.write('\n2026-10-20：已完成来源核对、192857行提取、数据清洗、SQL/pandas对账；生成5表4关系11DAX3页PBIP。当前进入Desktop实际刷新与交互核对；尚无已验证PBIX，Excel核对待做。用户手动打开工程待响应。\n')
with (r/'全局工作台.md').open('a',encoding='utf-8') as h:h.write('\n2026-10-20 / project-0011：Chicago311 PowerBI完成数据准备及PBIP生成（192857原始、161706纳入、156576完成/5030开放/100取消）。数据与模型一致性检查通过；Desktop刷新/视觉、Excel核对、PBIX另存待做，Portfolio尚未开始。project-0007已另存带Oct2026项目日期的一页简历。\n')
with (r/'全局复利与踩坑日志.md').open('a',encoding='utf-8') as h:h.write('\n2026-10-20 / Chicago311：源duplicate标记不同于重复主键；Canceled不能用非Completed条件归入开放积压。保留原始分页和源标记，分别统计关闭/开放/取消并三方对账。快照无法证明历史状态流水，全窗口创建cohort未包括更早积压。Windows Computer Use模态对话框可能无法稳定定向，捕获到非目标画面时停止盲目输入，改为请求用户打开工程。证据project-0011/04-验证与测试/data-validation.json、model-consistency.json及执行记录。\n')
print('Date verified; resume remains one page; logs updated')
