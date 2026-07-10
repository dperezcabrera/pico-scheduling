# Architecture

```
@scheduled(every=/cron=)          SchedulerRegistrar (@component)
        |                                  |
   marks method meta          @configure: scan locator -> add_job per method
        |                                  |
   component class  <---- container.get(cls) on every tick ----+
                                           |
                              BackgroundScheduler (APScheduler 3.x)
                              @cleanup: shutdown(wait=False)
```

## Design decisions

- **Marker decorator + registrar** (same idiom as pico-celery's `@task`): the
  decorator only stores metadata on the function; discovery happens once at
  container startup by scanning registered component classes. No import-order
  coupling, no global scheduler state.
- **Container resolution per run**: jobs call `container.get(cls)` on every
  tick, so singleton components share state across runs and prototype
  components get a fresh instance per run — scope semantics are the
  container's, not the scheduler's.
- **One scheduler, lazy**: the `BackgroundScheduler` thread is created only if
  at least one `@scheduled` method exists and `scheduling.enabled` is true.
  Zero cost otherwise.
- **Failure isolation**: the job wrapper catches everything, logs the
  traceback and returns — a raising job never kills the scheduler thread or
  the other jobs.
- **Async via asyncio.run in the worker thread**: async methods run on a
  private loop per tick, never on the application's loop. Loop-integrated
  work should enqueue instead (see FAQ).
- **APScheduler 3.x pinned `< 4`**: the 4.x line has been pre-release for
  years; migration will be a deliberate major, not a dependabot surprise.
