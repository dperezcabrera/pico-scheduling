# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-10

### Added

- `@scheduled(every=seconds)` and `@scheduled(cron="...")` marker decorator for component methods (sync and async).
- `SchedulerRegistrar`: discovers scheduled methods at container startup, runs them on a `BackgroundScheduler`, stops on container shutdown.
- `scheduling.enabled` setting (zero-config, defaults to on).
- Auto-discovery via the `pico_boot.modules` entry point.
