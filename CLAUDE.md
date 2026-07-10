Read and follow ./AGENTS.md for project conventions.

## Pico Ecosystem Context

pico-scheduling — Scheduled method execution: @scheduled(every=/cron=) on components via APScheduler 3.x. Auto-discovered via the `pico_boot.modules` entry point. See it wired with the whole ecosystem in the flagship use case (pico-boot docs).

## Key Reminders

- pico-ioc dependency: `>= 2.2.0`; apscheduler `>= 3.10, < 4`
- **NEVER change `version_scheme`** in pyproject.toml. It MUST remain `"post-release"`.
- requires-python >= 3.11
- Commit messages: one line only
