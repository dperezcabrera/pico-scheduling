# Troubleshooting

## My job never runs

- Is the component's module listed in `init(modules=[...])` (or discoverable
  by pico-boot)? The registrar only scans registered components.
- Is `scheduling.enabled` true? The kill-switch silently disables everything.
- `@scheduled` must decorate a method of a `@component` class — plain
  functions are not discovered.

## Jobs stopped when my test ended

That is by design: the scheduler stops on `container.shutdown()`. Keep the
container alive as long as you need the schedule.

## `ValueError: @scheduled requires exactly one of every= or cron=`

Both triggers were given, or neither. Pick one per method; use two methods
for two schedules.

## A run is skipped with a "maximum number of running instances" warning

APScheduler's default: a still-running job skips its next fire. Keep
scheduled work shorter than its interval, or delegate the heavy part to
pico-celery and keep the scheduled method as a dispatcher.

## My async job seems to block other jobs

Each tick runs in the scheduler's worker thread via `asyncio.run`. Long-lived
awaits hold that thread like any long sync job would — same remedy as above.
