def reschedule_value(value, default=45):
    return default if value is None else int(value)
