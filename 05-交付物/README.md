# Chicago 311 Service Operations Analytics

Created October 2026 by Sunny Li. The PBIP project has been refreshed successfully in Power BI Desktop. All 31 live DAX / Python metric comparisons passed. All three pages were inspected directly in the native Desktop window, including a service filter and reset test on the backlog page. A genuine standalone [Chicago311.pbix](powerbi/Chicago311.pbix) was exported through Desktop Save As, with embedded data and all three report pages. Excel reconciliation remains pending.

See the [main GitHub README](../README.md) for the complete project overview, download links, repository guide, validation scope, and reproduction notes. See [resume project bullets](Resume_Project_Bullets.md) for truthful English resume wording.

## Business question
Which service types and community areas warrant investigation for long closure times and remaining open requests?

## Scope
Three service types: graffiti removal, street potholes, street light outages. Requests created October 1, 2025 through September 30, 2026. Current administrative statuses retrieved 2026-10-20 18:57:04 America/Chicago. This is a fixed cohort study, not a reconstruction of historical citywide backlog.

Official source: https://data.cityofchicago.org/d/v6vf-nfxy

## Data preparation completed
- 192,857 original requests retained in four immutable extraction pages with query URLs and SHA-256 hashes.
- One request per sr_number; 0 duplicate identifiers in this extraction.
- 31,151 records flagged as duplicates excluded from operating KPIs, retained for audit. This flag is different from a repeated identifier.
- 161,706 included requests: 156,576 completed, 5,030 open, 100 canceled.
- Canceled requests are retained as a separate status and are not counted as open backlog.
- Completed records require a present, nonnegative closure duration and a close timestamp no later than extraction to enter duration measures.

## Current independently checked findings
Street potholes account for 3,234 of 5,030 open cohort requests (64.3%). Across the full included cohort, 2,661 open requests are over 90 days old (52.9% of open requests). Median closed duration is 0.91 days versus a P90 of 12.77 days. Compare service types separately before comparing community areas. Differences in request complexity and submission behavior may explain differences in processing times; this analysis does not establish causation.

## Power BI project
Open `powerbi/Chicago311.pbip` using Power BI Desktop. If the canvas is empty on first load, use Home > Refresh. The semantic model imports the project-local CSV snapshots through typed Power Query transformations. Model: FactRequests, DimService, DimArea, DimCreatedDate, DimClosedDate; four single-direction many-to-one relationships. Separate created and closed date dimensions support separate arrival and closure timelines.

Pages: Operations overview, Closure performance, Cohort backlog. The live semantic model is saved as TMDL in `powerbi/Operations.SemanticModel/definition`. It includes eleven explicit DAX measures, a hidden age-band sort column, and a zero-safe invalid-date count. The current TMDL is authoritative; the original bootstrap measure listing predates the zero-safe correction.

Validation evidence: `04-验证与测试/live-dax-results.json`, `live-metric-reconciliation.json`, and `native-window-review.json` in the project root. The direct window review was used at the user's request because the CLI Desktop Bridge could not match the open report folder. This is not a claim that CLI screenshot automation passed. The final report uses modern multi-value cards, teal/amber median/P90 series, populated community matrices, chronological age bands, and visible service dropdowns. Unknown community areas remain visible rather than being silently excluded.

## Reproduce
Use a Python environment with pandas and NumPy. `extract.py` retrieves the source; `prepare_model_data.py` prepares CSV and SQLite data. Preserve the supplied snapshot for reproducing these findings. Open the current `powerbi/Chicago311.pbip` for the finished report layout. `build_powerbi.py` and `polish_report.mjs` are earlier bootstrap-stage scripts: do not rerun them over the current Desktop-saved TMDL project, because they can replace later changes. After moving the folder, update the five CSV paths through Power Query and refresh. `verify_live_model.mjs` captures actual local DAX results; `reconcile_live_metrics.py` compares them with the CSV snapshot. SQL analysis executes in SQLite, not SQL Server. No scheduled refresh or incremental refresh has been validated. Save a real `.pbix` through Desktop if a single-file export is needed; do not rename a PBIP or ZIP.

## Limitations
Administrative closure does not prove resident-confirmed resolution. No official SLA is asserted; age thresholds are descriptive. Earlier unresolved requests outside the creation window are excluded. Source data can change during pagination, so this is an extraction snapshot rather than a transactionally frozen source version. No claim of staffing savings, causal improvements, or deployed Power BI Service report is made.
