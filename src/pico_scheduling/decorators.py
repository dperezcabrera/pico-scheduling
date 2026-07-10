"""Marker decorator: stores the schedule on the method; the registrar
picks it up at container startup (same idiom as pico-celery's @task)."""

SCHEDULED_META = "_pico_scheduling_meta"


def scheduled(*, every: float | None = None, cron: str | None = None):
    """Run a component method on a schedule.

    Exactly one of ``every`` (seconds between runs) or ``cron`` (standard
    5-field crontab expression) must be given. Sync and async methods are
    both supported.
    """
    if (every is None) == (cron is None):
        raise ValueError("@scheduled requires exactly one of every= or cron=")
    if every is not None and every <= 0:
        raise ValueError("@scheduled(every=...) requires a positive number of seconds")

    def dec(fn):
        setattr(fn, SCHEDULED_META, {"every": every, "cron": cron})
        return fn

    return dec
