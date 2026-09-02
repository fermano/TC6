"""Seed-only helper for the requested regression."""

def replay_grace_seconds(value, default=30):
    return default if value is None else int(value)
