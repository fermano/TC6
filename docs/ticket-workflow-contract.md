# Delivery workflow contract

Delivery owner keys are trimmed and lowercased. Runs of internal Unicode
whitespace are collapsed to one ASCII space. Blank owners use `engineering-ops`.

Owner filters preserve input record order and use the same canonicalization rules
as routing. A missing owner selection means no filtering; an explicitly empty
selection returns no records.

Delivery summaries expose owner and status by default. Callers may opt into a
trimmed, lowercased source field; blank or missing opted-in sources are reported
as `unknown`.
