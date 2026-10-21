# Chicago 311 Service Operations Analytics

**Power BI · Power Query · DAX · SQL (SQLite) · Python / pandas**  
Portfolio project by Sunny Li | October 2026

Which services and community areas warrant investigation for long closure times and remaining open requests? This project turns 192,857 Chicago 311 records into a three-page Power BI report, with a documented cohort definition and independent checks of live DAX results.

**[Download the Power BI report](https://github.com/Supersunny7/chicago-311-powerbi-analytics/releases/download/v1.0.0/Chicago311.pbix)** · **[Browse the PBIP source](05-交付物/powerbi/Chicago311.pbip)** · **[Metric validation evidence](04-验证与测试/live-metric-reconciliation.json)**

The PBIX is a downloadable, interactive Desktop report. This repository does not provide a publicly hosted Power BI Service dashboard.

## Business question and findings

The analysis supports an investigation sequence: understand demand, compare closure-time distributions, then inspect older open requests by service and community area.

| Metric | Validated result |
|---|---:|
| Original records | 192,857 |
| Source-flagged duplicate records excluded from KPIs | 31,151 |
| Included requests | 161,706 |
| Completed / open / canceled | 156,576 / 5,030 / 100 |
| Share currently completed | 96.8% |
| Median closed duration | 0.91 days |
| P90 closed duration | 12.77 days |
| Open requests over 90 days | 2,661; 52.9% of open requests |

- **The typical duration does not describe the slower tail.** Median and P90 provide different views of completed requests; open requests are analyzed separately rather than treated as completed observations.
- **Street potholes account for 64.3% of remaining open requests:** 3,234 of 5,030. This identifies an investigation priority, without establishing why those requests remain open.
- **Community comparisons need service context.** Select one service before interpreting area differences, and keep unknown community areas visible as a data-quality category.

These are descriptive findings. No causal improvement, staffing savings, official SLA violation, or resident-confirmed resolution is asserted.

## Data scope

Source: [City of Chicago — 311 Service Requests](https://data.cityofchicago.org/d/v6vf-nfxy), dataset `v6vf-nfxy`.

- **Creation window:** October 1, 2025 inclusive to October 1, 2026 exclusive.
- **Services:** graffiti removal, street potholes, and street light outages.
- **Status snapshot:** October 20, 2026, approximately 18:57 America/Chicago.
- **Grain:** one record per service request (`sr_number`). No repeated identifiers were found in this extraction. A source duplicate flag is a separate concept from repeated IDs.
- **Privacy-conscious selection:** the extraction selects request identifiers, service/status fields, timestamps, area/ward, and operational flags; it does not select names, street addresses, or precise coordinates.

The snapshot follows a fixed creation cohort. Its open count excludes unresolved requests created before the window; it is **not total historical citywide backlog**. The source is paginated and can change during extraction.

## Report pages

| Page | Purpose | Interaction |
|---|---|---|
| Operations overview | Request totals, status context, monthly arrivals, service mix | Select service type |
| Closure performance | Median versus P90, completion timeline, community comparison | Compare within a service |
| Cohort backlog | Open age, requests over 90 days, service concentration, area shortlist | Filter service; investigate older requests |

Each page has its own service slicer. Pages do not claim synchronized selections. Age bands use a hidden sort column to preserve chronological order. The 90-day threshold is an analysis choice, not an official SLA.

## Workflow and skills demonstrated

1. **Extract:** retrieve four paginated JSON files using the public Socrata endpoint; retain query URLs and SHA-256 hashes in the source manifest.
2. **Clean:** preserve source-flagged duplicates for audit but exclude them from operating KPIs; separate completed, open, and canceled statuses; validate date availability, order, and snapshot boundaries.
3. **Analyze in SQL and Python:** use SQLite CTEs and `LAG` for monthly comparisons; compute distributions and grouped checks in pandas.
4. **Model in Power BI:** build one fact table and four dimensions with single-direction relationships. Separate created-date and closed-date dimensions support arrivals and completions without confusing the two timelines.
5. **Calculate:** use eleven explicit DAX measures for counts, shares, median, continuous P90, and open-age indicators. Treat an empty invalid-date count as zero.
6. **Validate and communicate:** compare 31 live DAX results against independent pandas calculations; inspect all three native Desktop pages and test the backlog service slicer and reset.

The report imports prepared CSV snapshots through typed Power Query transformations. Most cleaning is performed in Python; this project does not claim that every cleaning step was implemented in Power Query.

## Open the report

Download `05-交付物/powerbi/Chicago311.pbix` using GitHub's raw download option, then open it in a recent Power BI Desktop version supporting PBIR. The file contains an imported data model, so viewing the saved snapshot does not require a source refresh or a Power BI Service sign-in.

For source control, open `05-交付物/powerbi/Chicago311.pbip`. Keep `Operations.Report` and `Operations.SemanticModel` beside it. PBIP is the folder-based source; PBIX is the standalone Desktop deliverable. Do not convert between them by renaming extensions.

**Refreshing on another computer:** the five CSV sources currently use local absolute paths. Update those paths in Power Query to the CSV files under `03-执行内容/data` before refreshing. The included data is a fixed historical snapshot, not a live feed.

## Repository guide

| Location | Contents |
|---|---|
| `01-需求与原始资料/` | Source snapshot, metadata, extraction manifest |
| `03-执行内容/extract.py` | Public API extraction |
| `03-执行内容/prepare_model_data.py` | Cleaning, CSV model inputs, SQLite outputs |
| `03-执行内容/*_operations.sql` | Monthly and service analysis |
| `03-执行内容/data/` | Prepared tables and analysis outputs |
| `03-执行内容/verify_live_model.mjs` | Capture live Desktop DAX results through the local Microsoft MCP tool |
| `03-执行内容/reconcile_live_metrics.py` | Compare captured DAX with pandas calculations |
| `04-验证与测试/` | Data, metric, report, and native-window verification evidence |
| `05-交付物/powerbi/` | PBIX deliverable and PBIP / PBIR / TMDL source |
| `05-交付物/数据刷新与三页验收说明.md` | Chinese explanation and interview walkthrough |

Python analysis requires pandas and NumPy. The live verification helper additionally requires the local Microsoft Power BI Modeling MCP installation; its current local setup paths are documented in the code. It is not a portable one-command verification environment.

For the preserved snapshot, rerun the independent reconciliation from the project root:

```powershell
python "03-执行内容/reconcile_live_metrics.py"
```

`extract.py` and `prepare_model_data.py` write their outputs into this project. Run them in a separate copy when retrieving new data so the historical evidence is preserved. A new extraction may produce different statuses and counts.

`build_powerbi.py` and `polish_report.mjs` are earlier authoring-stage scripts, not current rebuild commands. Do not run them over the Desktop-saved TMDL project: they can replace later edits. The committed PBIP source is the current report definition.

## Validation and boundaries

- Live DAX / pandas reconciliation: **31 comparisons passed**, including totals, service breakdowns, quantiles, and age bands.
- Meaningful status check: included = completed + open + canceled.
- Native Desktop review: three pages render data; median/P90 colors differ; matrices contain rows; service dropdown sizing was corrected.
- Backlog interaction test: selecting street potholes shows 3,234 open requests; clearing the selection restores 5,030.
- CLI report validation previously returned zero errors with one warning about an unreachable schema. Subsequent slicer sizing was saved through Desktop. Native window inspection was used at the user's request; CLI Desktop Bridge screenshot automation is not claimed as passed.

The project does not yet include a Power BI Service deployment, scheduled/incremental refresh, an Excel reconciliation workbook, or a mobile/accessibility audit. Administrative closure is not confirmation that a resident's issue was resolved. Closed-request durations alone do not estimate time to resolution for all requests because still-open requests are excluded from those duration statistics.

## Data and attribution

The underlying records are provided by the City of Chicago. Keep the source attribution and extraction manifest when sharing this analysis; consult the source portal's applicable data terms. No affiliation with or endorsement by the City of Chicago is implied.
