# Metric Dictionary

Business measures exclude records flagged as duplicates or legacy records. Original rows remain available for audit. The fact-table grain is one service request.

| Measure | Definition | Interpretation |
|---|---|---|
| Requests | Included requests across completed, open, and canceled statuses | One row per request |
| Closed Requests | Included requests marked Completed or Closed | Administrative status, not resident confirmation |
| Open Cohort Requests | Included requests with status Open | Excludes canceled requests and older carry-in backlog |
| Closed Share | Closed Requests / Requests | Denominator includes cancellations; not SLA attainment |
| Valid Closed Requests | Closed requests with eligible closure timestamps | Invalid dates exclude duration observations, not the request total |
| Median Closed Days | Median eligible closed duration in fractional days | Recomputed within the active filter context |
| P90 Closed Days | Continuous 90th percentile of eligible closed durations | Linear interpolation; never average subgroup P90 values |
| Median Open Age Days | Median fractional days since creation at extraction | Fixed snapshot time rather than TODAY() |
| Open Over 90 Days | Open requests older than 90 complete 24-hour periods | Analysis threshold, not an official SLA |
| Open Over 90 Share | Open Over 90 Days / Open Cohort Requests | Blank when the denominator is zero |
| Invalid Closed Dates | Closed requests without an eligible duration | Count returns zero when no such rows exist; missing durations are not imputed as zero |

`DimCreatedDate` supports arrival trends; `DimClosedDate` supports completion trends. Separate role-playing date dimensions avoid ambiguous active relationships.

Age bands represent 0-7, greater than 7-30, greater than 30-90, and over 90 fractional days. The hidden sort column preserves chronological order. Empty bands may not appear.

Compare communities within the same service type. A mixed-service median is not a fair standalone measure of community performance. Unknown community areas are retained as a data-quality category.
