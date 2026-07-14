DEFAULT_OWNER = "engineering-ops"
UNKNOWN_SOURCE = "unknown"


def normalize_delivery_owner(owner: str | None) -> str:
    """Return the routing key used by delivery workflows."""
    normalized = " ".join((owner or "").strip().lower().split())
    return normalized or DEFAULT_OWNER


def filter_delivery_records(
    records: list[dict],
    owners: list[str | None] | None = None,
) -> list[dict]:
    """Filter records by canonical owner without changing their order."""
    if owners is None:
        return list(records)

    selected_owners = {normalize_delivery_owner(owner) for owner in owners}
    return [
        record
        for record in records
        if normalize_delivery_owner(record.get("owner")) in selected_owners
    ]


def delivery_summary(record: dict, include_source: bool = False) -> dict:
    """Return stable summary fields, optionally including normalized source."""
    summary = {
        "owner": normalize_delivery_owner(record.get("owner")),
        "status": record["status"],
    }
    if include_source:
        normalized_source = (record.get("source") or "").strip().lower()
        summary["source"] = normalized_source or UNKNOWN_SOURCE
    return summary
