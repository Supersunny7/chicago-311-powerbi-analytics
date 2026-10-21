# Refresh, Validation, and Report Review

## What was done
1. Diagnosed blank cards: report definitions and tables existed, but imported data had not loaded. Checked five CSV paths and corrected a Unicode path-encoding issue.
2. Completed an actual Desktop refresh. An earlier external XMLA Full refresh encountered a PackageSession error; Desktop Refresh now succeeded after reopening.
3. Captured live DAX results through the local model tool and compared 31 quantities, service breakdowns, quantiles, and age bands against pandas. All passed with a duration tolerance of 1e-8 days.
4. Made the invalid-date count explicitly return zero when no records qualify; added chronological sorting for age bands.
5. Migrated headline metrics to modern multi-value cards, distinguished median/P90 colors, and used populated community matrices.
6. Inspected three native Desktop pages and corrected dropdown height. Filtering backlog to street potholes produced 3,234 open requests and 1,327 over 90 days; clearing restored 5,030 and 2,661.
7. Exported Chicago311.pbix through Desktop Save As, preserved the PBIP source, checked archive integrity, and reopened all three pages from the exported file without a source refresh.
8. Published the source and PBIX to GitHub; verified public access and a matching download hash.

## Findings to explain
Median closed duration is approximately 0.91 days versus a P90 of 12.77 days. Of remaining open requests, 52.9% are over 90 days old and 64.3% are street potholes. These are investigation signals, not evidence of the causes of delay.

## Interview wording
I compared live Power BI measures with independent Python calculations rather than checking only a rendered chart. I separated request statuses and date roles, used median and P90 to describe closed-request durations, and analyzed open requests separately. I documented the fixed-cohort boundary and the difference between administrative closure and verified resolution.

## Limits of verification
Native Desktop review passed. CLI Desktop Bridge screenshot automation did not pass because folder matching was unavailable. No cloud deployment, scheduled refresh, Excel reconciliation workbook, or quantified operational improvement is claimed.
