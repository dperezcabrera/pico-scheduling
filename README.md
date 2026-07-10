# pico-scheduling

[![PyPI](https://img.shields.io/pypi/v/pico-scheduling.svg)](https://pypi.org/project/pico-scheduling/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/dperezcabrera/pico-scheduling)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![CI (tox matrix)](https://github.com/dperezcabrera/pico-scheduling/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/dperezcabrera/pico-scheduling/branch/main/graph/badge.svg)](https://codecov.io/gh/dperezcabrera/pico-scheduling)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dperezcabrera_pico-scheduling&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dperezcabrera_pico-scheduling)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=dperezcabrera_pico-scheduling&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=dperezcabrera_pico-scheduling)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dperezcabrera_pico-scheduling&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=dperezcabrera_pico-scheduling)
[![PyPI Downloads](https://img.shields.io/pypi/dm/pico-scheduling)](https://pypi.org/project/pico-scheduling/)
[![Docs](https://img.shields.io/badge/Docs-pico--scheduling-blue?style=flat&logo=readthedocs&logoColor=white)](https://dperezcabrera.github.io/pico-scheduling/)
[![Interactive Lab](https://img.shields.io/badge/Learn-online-green?style=flat&logo=python&logoColor=white)](https://dperezcabrera.github.io/pico-learn/)

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
