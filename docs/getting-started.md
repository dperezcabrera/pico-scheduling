# Getting Started

## Prerequisites

- Python >= 3.11
- pico-ioc >= 2.2.0 (pico-boot recommended for auto-discovery)
- APScheduler >= 3.10, < 4 (installed automatically)

## Install

```bash
pip install pico-scheduling
```

## Key concepts

| Piece | What it does |
|---|---|
| `@scheduled(every=N)` | Runs the method every N seconds |
| `@scheduled(cron="m h dom mon dow")` | Runs the method on a 5-field crontab schedule |
| `SchedulerRegistrar` | Discovers marked methods at startup, starts a `BackgroundScheduler`, stops it on shutdown |
| `scheduling.enabled` | Config kill-switch (default `true`) |

## Semantics

- Exactly one of `every` / `cron` per method; `every` must be positive. Both are validated at import time.
- Each run resolves the component through the container: singletons share state across runs, prototype scope gets a fresh instance per run.
- Async methods are supported; they run via `asyncio.run` in the scheduler's worker thread.
- A raising job is logged with its traceback and the schedule continues.
- No `@scheduled` methods in the container means no scheduler thread at all.

## Configuration

```yaml
scheduling:
  enabled: false   # disables every job (useful in tests and one-off scripts)
```
