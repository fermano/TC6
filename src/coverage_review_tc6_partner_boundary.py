def resolve_partner_value(payload, default=45):
    value = payload.get("grace_seconds")
    if value is None:
        value = payload.get("graceSeconds")
    return default if value in (None, "") else value
