# Resume project entry

## Recommended version

**Chicago 311 Service Operations Analytics** | Power BI, DAX, Power Query, SQL, Python | Oct 2026

- Analyzed 192,857 Chicago 311 records using Python and SQL; separated completed, open, and canceled requests and excluded 31,151 source-flagged duplicates from operating metrics.
- Built a three-page Power BI report with a five-table dimensional model and 11 DAX measures to compare median/P90 closure times and investigate aging open requests by service and community area.
- Validated 31 live DAX results against independent Python calculations; identified street potholes as 64.3% of remaining open requests and documented cohort and administrative-status limitations.

## Compact version for a one-page resume

**Chicago 311 Service Operations Analytics** | Power BI, SQL, Python | Oct 2026

- Cleaned and analyzed 192,857 service requests; built a three-page Power BI report with Power Query imports, a five-table model, and 11 DAX measures for closure times and open-request aging.
- Reconciled 31 live Power BI metrics with Python; found that street potholes represented 64.3% of open cohort requests and distinguished administrative closure from verified resolution.

## Links

Resume project link: https://github.com/Supersunny7/chicago-311-powerbi-analytics

Direct PBIX download: https://github.com/Supersunny7/chicago-311-powerbi-analytics/releases/download/v1.0.0/Chicago311.pbix

Link recruiters to the repository README; it provides the downloadable PBIX and the PBIP source. Do not label this as a hosted live dashboard: the interactive report runs in Power BI Desktop.

## Interview explanation

“I wanted to understand which requests warranted investigation rather than report only an overall completion rate. I separated statuses carefully, used both median and P90 for closed requests, and analyzed open requests separately. I validated the live Power BI measures against Python and used service filters to avoid misleading community comparisons. The results describe a fixed cohort at extraction, not all historical citywide backlog.”

## Claims to avoid

Do not claim Advanced Excel, SQL Server, cloud data engineering, real-time reporting, Power BI Service deployment, or quantified operational savings from this project. SQL analysis currently runs in SQLite, and the Power BI model uses imported CSV snapshots.
