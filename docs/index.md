# pico-scheduling

`@scheduled` on pico components: interval and cron jobs that start with the container and stop with it.

## Install

```bash
pip install pico-scheduling
```

## 30-second example

```python
from pico_ioc import component
from pico_scheduling import scheduled

@component
class Reports:
    @scheduled(every=300)
    def refresh_cache(self):
        ...

    @scheduled(cron="0 3 * * *")
    async def nightly_rollup(self):
        ...
```

No wiring: pico-boot discovers the module, the registrar discovers the methods, jobs run on a background scheduler and shut down with the container.
