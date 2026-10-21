from pathlib import Path
import json,pandas as pd,sqlite3,math
p=Path(__file__).resolve().parents[1];s=json.loads((p/'03-执行内容/data/summary.json').read_text());out=p/'05-交付物'
(out/'README.md').write_text(f'''# Chicago 311 Service Operations Analytics

Power BI portfolio project in progress. Created October 2026 by Sunny Li. Desktop refresh, visual validation, Excel reconciliation, and PBIX export are pending; generated files are not evidence of successful Desktop execution.

## Business question
Which service types and community areas warrant investigation for long closure times and remaining open requests?

## Scope
Three service types: graffiti removal, street potholes, street light outages. Requests created October 1, 2025 through September 30, 2026. Current administrative statuses retrieved {s['asof_local'][:19]} America/Chicago. This is a fixed cohort study, not a reconstruction of historical citywide backlog.

Official source: https://data.cityofchicago.org/d/v6vf-nfxy

## Data preparation completed
- {s['raw_rows']:,} original requests retained in four immutable extraction pages with query URLs and SHA-256 hashes.
- One request per sr_number; {s['duplicate_ids_removed']} duplicate identifiers in this extraction.
- {s['source_duplicate_flag']:,} records flagged as duplicates excluded from operating KPIs, retained for audit. This flag is different from a repeated identifier.
- {s['included_requests']:,} included requests: {s['closed_requests']:,} completed, {s['open_cohort_requests']:,} open, {s['canceled_requests']:,} canceled.
- Canceled requests are retained as a separate status and are not counted as open backlog.
- Completed records require a present, nonnegative closure duration and a close timestamp no later than extraction to enter duration measures.

## Current independently checked findings
Street potholes account for {s['services'][0]['open']:,} of {s['open_cohort_requests']:,} open cohort requests. Compare service types separately before comparing community areas. Differences in request complexity and submission behavior may explain differences in processing times.

## Power BI project
Open `powerbi/Chicago311.pbip` using Power BI Desktop. If the canvas is empty on first load, use Home > Refresh. The semantic model imports the project-local CSV snapshots through typed Power Query transformations. Model: FactRequests, DimService, DimArea, DimCreatedDate, DimClosedDate; four single-direction many-to-one relationships. Separate created and closed date dimensions support separate arrival and closure timelines.

Pages: Operations overview, Closure performance, Cohort backlog. Eleven DAX measures are in `powerbi/DAX_measures.txt`.

After opening: confirm no data/model errors, refresh, compare KPIs against the validation file, exercise service filters, inspect all three pages, and save as a real `.pbix` through Desktop. Do not rename a PBIP or ZIP to PBIX.

## Reproduce
Use a Python environment with pandas and NumPy. Run `03-执行内容/extract.py`, then `prepare_model_data.py`, then `build_powerbi.py` from the project root. Extraction requires public internet access. Power BI uses absolute local CSV paths; after moving the folder, regenerate the model to update them. SQL analysis currently executes in SQLite, not SQL Server. No scheduled refresh or incremental refresh has been validated.

## Limitations
Administrative closure does not prove resident-confirmed resolution. No official SLA is asserted; age thresholds are descriptive. Earlier unresolved requests outside the creation window are excluded. Source data can change during pagination, so this is an extraction snapshot rather than a transactionally frozen source version. No claim of staffing savings, causal improvements, or deployed Power BI Service report is made.
''',encoding='utf-8')
(out/'指标字典.md').write_text('''# 指标字典

所有业务指标排除 duplicate=true 和 legacy_record=true，保留原始记录。

| 指标 | 定义 | 注意事项 |
| --- | --- | --- |
| Requests | 纳入请求数，含Completed/Open/Canceled | 一行一请求 |
| Closed Requests | status=Completed或Closed | 行政状态，不是居民确认 |
| Open Cohort Requests | status=Open | 不含Canceled；不是全部历史积压 |
| Closed Share | Closed Requests / Requests | 不是SLA达标率；分母含取消 |
| Valid Closed Requests | 已关闭且日期有效 | 日期缺失只排除时长，不排除请求总数 |
| Median Closed Days | 合格关闭记录的处理天数中位数 | 连续天数；筛选下重算 |
| P90 Closed Days | 合格关闭记录的90%分位数，线性插值 | 不取分组P90的平均 |
| Median Open Age Days | 开放请求在提取时点的等待天数中位数 | 固定as-of，不用TODAY使截图漂移 |
| Open Over 90 Days | 等待时间大于90×24小时的开放请求 | 分析阈值，不是官方违约 |
| Open Over 90 Share | Open Over 90 / Open Cohort Requests | 没有开放请求时DAX返回空 |
| Invalid Closed Dates | 已关闭但无有效时长的请求数 | 不把缺失填0 |

时间维度：DimCreatedDate按创建日分析到达；DimClosedDate按关闭日分析完成。当前模型使用独立角色日期维度，避免两条同时指向同一日期表的活跃关系引起歧义。

服务之间处理复杂程度不同；先按服务筛选，再比较地区，不能把全服务混合中位数解释为地区绩效。
''',encoding='utf-8')
(out/'第一阶段实际操作与面试讲解.md').write_text(f'''# 第一阶段实际操作与面试讲解

## 已完成什么
1. 核对官方数据字段，确认有请求编号、请求类型、当前状态、创建/关闭/修改时间、地区及重复标志。
2. 先统计请求类型规模，选取涂鸦、坑洞、路灯三类，控制第一版范围；没有将信息咨询电话混入维修效率分析。
3. 下载2025-10-01至2026-09-30创建的{s['raw_rows']:,}条记录。保留原始分页JSON、查询条件和SHA-256。
4. 建立一行一请求的数据表，区分“同一ID重复行”和“源系统重复请求标记”。本次ID唯一，源系统标记重复{s['source_duplicate_flag']:,}条。
5. 分开Completed、Open和Canceled。纳入{s['included_requests']:,}条，已关闭{s['closed_requests']:,}，开放{s['open_cohort_requests']:,}，取消{s['canceled_requests']:,}，三者加总严格对账。
6. 只对合格的关闭记录计算处理时长；用固定提取时点计算开放等待时长，不用当前日期让结果每天漂移。
7. 执行SQLite SQL条件聚合、CTE和LAG月度比较，并与独立pandas人数对账。SQL当前不是SQL Server；不新增未经完成的数据库技能。
8. 生成Power BI工程：一张事实表、四张维度表、四条关系、十一项DAX、三页报表；Power Query导入CSV时显式设类型。

## 为什么这么做
请求创建月份回答需求到达，关闭月份回答处理完成，不能混成同一条趋势。当前状态快照缺少历史变更记录，不能凭空画每个历史月的真实积压。Canceled也不该列入未处理工作量。

## 已验证与未验证
数据检查已通过，详见04-验证与测试/data-validation.json。Desktop实际刷新、DAX引擎输出、三页视觉及交互、Excel核对和PBIX另存仍待完成。生成JSON/PBIP不等于实际Power BI已运行。

## 面试英文
I used recent Chicago 311 requests to study closure times and the remaining workload for three service types. I defined the grain as one service request, separated canceled requests from open backlog, and retained source-flagged duplicates for audit while excluding them from operating metrics. I also separated request creation dates from closure dates. The backlog measure describes the selected creation cohort at extraction, rather than the city's full historical backlog.

## 你需要能回答
- 为什么193k原始请求变成161k纳入记录？
- 源系统标记重复和主键重复有什么区别？
- 为什么取消不能当作开放请求？
- 为什么中位数/P90必须在明细筛选后重新算？
- 为什么这个数据不能证明历史积压或服务因果效果？

## 下一步
实际打开powerbi/Chicago311.pbip并刷新；核对全量及各服务筛选KPI；检查关闭日期角色和三个页面；完成Excel抽样对账；通过后另存真实PBIX。按用户顺序，之后再建立Portfolio网站，不把进行中的项目标为完成。
''',encoding='utf-8')
# Additional independent export/model consistency checks.
model=json.loads((out/'powerbi/Operations.SemanticModel/model.bim').read_text())['model']
checks={}
for table in model['tables']:
 f=pd.read_csv(p/'03-执行内容/data'/(table['name']+'.csv'))
 checks[table['name']+'_columns_match']=list(f.columns)==[c['name'] for c in table['columns']]
 if table['name'].startswith('Dim'):
  key='service_type' if table['name']=='DimService' else 'community_area' if table['name']=='DimArea' else 'Date'
  checks[table['name']+'_key_unique']=bool(f[key].is_unique)
checks['all_relationships_one_direction']=all(r['crossFilteringBehavior']=='oneDirection' for r in model['relationships'])
assert all(checks.values())
(p/'04-验证与测试/model-consistency.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
with (p/'00-项目管理/执行记录.md').open('a',encoding='utf-8') as f:f.write(f"\n2026-10-20：第一阶段完成。下载{s['raw_rows']}行，排除{s['source_duplicate_flag']}源重复标记后{s['included_requests']}纳入；关闭{s['closed_requests']}、开放{s['open_cohort_requests']}、取消{s['canceled_requests']}。修正取消误算开放的早期草稿；最终7项数据检查通过。5表/4关系/11DAX/3页PBIP已生成；CSV及模型一致性检查通过。Power BI控制工具的模态对话框不稳定，曾捕获到非目标画面，已停止盲目操作并请求用户手动打开生成工程；未声称Desktop或PBIX完成。Portfolio按顺序尚未开始。\n")
print('Documentation and model consistency checks saved')
