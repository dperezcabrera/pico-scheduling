"""Discovers ``@scheduled`` methods and runs them on a background scheduler.

Jobs resolve their component through the container on every run, so
prototype-scoped components get a fresh instance per execution and
singletons are shared — same semantics as pico-celery task dispatch.
Async methods run via ``asyncio.run`` inside the scheduler's worker thread.
"""

import asyncio
import inspect
import logging
from typing import Callable, Type

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from pico_ioc import PicoContainer, cleanup, component, configure

from .config import SchedulingSettings
from .decorators import SCHEDULED_META

logger = logging.getLogger(__name__)


@component
class SchedulerRegistrar:
    def __init__(self, container: PicoContainer, settings: SchedulingSettings):
        self._container = container
        self._settings = settings
        self._scheduler: BackgroundScheduler | None = None

    @configure
    def start(self) -> None:
        if not self._settings.enabled:
            return
        jobs = list(self._discover())
        if not jobs:
            return
        self._scheduler = BackgroundScheduler()
        for cls, method_name, meta in jobs:
            trigger = (
                IntervalTrigger(seconds=meta["every"])
                if meta["every"] is not None
                else CronTrigger.from_crontab(meta["cron"])
            )
            self._scheduler.add_job(
                self._make_job(cls, method_name),
                trigger,
                id=f"{cls.__module__}.{cls.__qualname__}.{method_name}",
            )
        self._scheduler.start()
        logger.info("scheduler started with %d job(s)", len(jobs))

    @cleanup
    def stop(self) -> None:
        if self._scheduler is not None:
            self._scheduler.shutdown(wait=False)
            self._scheduler = None

    def _discover(self):
        locator = getattr(self._container, "_locator", None)
        metadata_map = getattr(locator, "_metadata", {}) if locator else {}
        for md in metadata_map.values():
            cls = getattr(md, "concrete_class", None)
            if not inspect.isclass(cls):
                continue
            for name, fn in inspect.getmembers(cls, inspect.isfunction):
                meta = getattr(fn, SCHEDULED_META, None)
                if meta is not None:
                    yield cls, name, meta

    def _make_job(self, cls: Type, method_name: str) -> Callable[[], None]:
        container = self._container

        def job() -> None:
            try:
                instance = container.get(cls)
                result = getattr(instance, method_name)()
                if inspect.iscoroutine(result):
                    asyncio.run(result)
            except Exception:  # noqa: BLE001
                # A failing job must not kill the scheduler thread; log and
                # let the next tick run.
                logger.exception("scheduled job %s.%s failed", cls.__name__, method_name)

        return job
