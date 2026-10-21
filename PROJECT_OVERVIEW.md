# Project Overview

**Chicago 311 Service Operations Analytics**  
Author: Sunny Li | October 2026  
[Public repository](https://github.com/Supersunny7/chicago-311-powerbi-analytics)

## Objective
Investigate service demand, closure-time distributions, and aging open requests across three Chicago 311 services. This is an independent Data Analyst portfolio project.

## Deliverables
- `README.md`: business findings, methods, repository guide, and limitations.
- `deliverables/powerbi/Chicago311.pbix`: genuine Desktop-exported report with imported data and three pages.
- `deliverables/powerbi/Chicago311.pbip`: source project, accompanied by PBIR report and TMDL model folders.
- `deliverables/Resume_Project_Bullets.md`: full and compact English resume entries.
- `deliverables/METRIC_DICTIONARY.md`: definitions and interpretation cautions.
- `validation/`: actual data, live DAX/Python, Desktop, export, and publication evidence.

## Completed work
Extracted 192,857 requests; excluded 31,151 source-flagged duplicates from operating KPIs while retaining them for audit. The included cohort contains 156,576 completed, 5,030 open, and 100 canceled requests.

Built five tables, four single-direction relationships, eleven explicit DAX measures, and a hidden age-band sort column. Typed Power Query imports load CSV snapshots; most cleaning is performed in Python, with SQL analysis in SQLite.

All 31 live DAX/Python comparisons passed. Three native Desktop pages were reviewed, dropdown sizing was corrected, and backlog filtering/reset was tested. A real PBIX was exported, reopened, and checked. Public GitHub access and the PBIX download were verified.

## Boundaries
Requests were created October 2025 through September 2026; statuses were captured October 20, 2026. This is a fixed cohort, not all historical citywide backlog. Closure is administrative, not resident-confirmed resolution. No official SLA or causal improvement is asserted.

Power BI Service deployment, scheduled/incremental refresh, an Excel reconciliation workbook, and mobile/accessibility auditing remain outside completed scope. Native window review is not a claim that CLI screenshot automation passed.
