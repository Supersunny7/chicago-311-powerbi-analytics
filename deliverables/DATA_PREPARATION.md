# Data Preparation and Interview Walkthrough

## Work performed
1. Reviewed the official schema for request identifiers, type, status, timestamps, community area, ward, and duplicate/legacy flags.
2. Selected graffiti removal, street potholes, and street light outages to keep repair-oriented services in a manageable first scope.
3. Retrieved 192,857 requests created October 2025 through September 2026; preserved four JSON pages, query URLs, and SHA-256 hashes.
4. Established one row per request. No repeated request identifiers were found; 31,151 records carried a source duplicate flag, which is a different concept.
5. Kept completed, open, and canceled requests separate. Included = 156,576 completed + 5,030 open + 100 canceled = 161,706.
6. Calculated durations only for eligible closed records, and open age at the fixed extraction timestamp.
7. Used SQLite conditional aggregation, CTEs, and LAG for monthly comparison; checked results independently with pandas.
8. Built the Power BI model with five tables, four relationships, eleven measures, and typed CSV imports.

## Why the definitions matter
Creation month describes incoming demand; closure month describes completed processing. Current statuses do not reconstruct historical month-end backlog. Canceled requests are not open workload.

## Validation status
The initial preparation phase was followed by successful Desktop refresh, 31 live DAX/Python comparisons, three-page native window review, and real PBIX export/reopen. See `../validation/` and `VALIDATION_WALKTHROUGH.md`. An Excel workbook and cloud deployment have not been completed.

## Interview explanation
I defined the grain as one service request, separated cancellations from open workload, and retained source-flagged duplicates for audit while excluding them from operating metrics. I used separate creation and closure dates and validated live Power BI results against Python. The open count describes the selected creation cohort at extraction, rather than all historical citywide backlog.

## Questions to prepare for
- Why does the raw count differ from the included count?
- How does a source duplicate flag differ from a repeated primary key?
- Why separate canceled requests from open requests?
- Why recompute quantiles from filtered detail records?
- What prevents this snapshot from proving historical backlog or causal effects?
