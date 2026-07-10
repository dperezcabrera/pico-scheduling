# pico-scheduling

[![PyPI version](https://img.shields.io/pypi/v/pico-scheduling.svg)](https://pypi.org/project/pico-scheduling/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/dperezcabrera/pico-scheduling/actions/workflows/ci.yml/badge.svg)](https://github.com/dperezcabrera/pico-scheduling/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/dperezcabrera/pico-scheduling/branch/main/graph/badge.svg)](https://codecov.io/gh/dperezcabrera/pico-scheduling)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://dperezcabrera.github.io/pico-scheduling/)

Scheduled method execution for the [pico ecosystem](https://github.com/dperezcabrera/pico-ioc): `@scheduled` on component methods, powered by APScheduler.

## Installation

```bash
pip install pico-scheduling
```

Auto-discovered by pico-boot; with plain pico-ioc add `"pico_scheduling"` to `init(modules=[...])`.

## Quick start

```python
from pico_ioc import component
from pico_scheduling import scheduled

@component
class Reports:
    @scheduled(every=300)          # every 5 minutes
    def refresh_cache(self): ...

    @scheduled(cron="0 3 * * *")   # 03:00 daily
    async def nightly_rollup(self): ...
```

Jobs start when the container starts and stop on `container.shutdown()`. Each run resolves the component through the container (prototype scope gives a fresh instance per run). A failing job is logged and does not stop the schedule. Sync and async methods both work.

Disable everything with config:

```yaml
scheduling:
  enabled: false
```

## Documentation

Full documentation: https://dperezcabrera.github.io/pico-scheduling/

## License

MIT
