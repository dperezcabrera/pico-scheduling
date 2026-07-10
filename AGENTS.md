# pico-scheduling

Scheduled method execution: @scheduled(every=/cron=) on components via APScheduler 3.x.

## Commands

```bash
pip install -e ".[dev]"
pytest tests/ -v
pytest --cov=pico_scheduling --cov-report=term-missing tests/
mkdocs serve -f mkdocs.yml
```

## Project Structure

```
src/pico_scheduling/
  __init__.py       # Public API
  decorators.py     # @scheduled marker (exactly one of every=/cron=)
  registrar.py      # SchedulerRegistrar: discovery + BackgroundScheduler lifecycle
  config.py         # SchedulingSettings (prefix "scheduling")
```

## Key Concepts

- Marker + registrar idiom (like pico-celery @task): decorator stores meta, @configure scan starts jobs.
- Each run resolves the component via container.get(cls): prototype scope = fresh instance per run.
- Async methods run via asyncio.run in the scheduler worker thread.
- A raising job logs and keeps its schedule; no scheduled methods -> no scheduler thread.
- `scheduling.enabled: false` disables everything.

## Boundaries

- APScheduler pinned `< 4` (4.x is pre-release); migration is a deliberate major
- Do not run jobs on the application's event loop
- Do not modify `_version.py`
