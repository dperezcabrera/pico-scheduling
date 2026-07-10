import sys
import time

import pytest
from pico_ioc import component

from pico_scheduling import SchedulerRegistrar, scheduled


@component
class Ticker:
    calls = 0
    async_calls = 0

    @scheduled(every=0.05)
    def tick(self):
        Ticker.calls += 1

    @scheduled(every=0.05)
    async def async_tick(self):
        Ticker.async_calls += 1


@component
class Broken:
    attempts = 0

    @scheduled(every=0.05)
    def explode(self):
        Broken.attempts += 1
        raise RuntimeError("boom")


@component
class Nightly:
    @scheduled(cron="0 3 * * *")
    def rollup(self):
        pass


def _wait_for(predicate, timeout=3.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.02)
    return False


def test_scheduled_methods_run_and_stop_on_shutdown(make_container):
    Ticker.calls = 0
    Ticker.async_calls = 0
    container = make_container(sys.modules[__name__])
    assert _wait_for(lambda: Ticker.calls >= 2)
    assert _wait_for(lambda: Ticker.async_calls >= 2)

    container.shutdown()
    settled = Ticker.calls
    time.sleep(0.2)
    assert Ticker.calls <= settled + 1


def test_failing_job_does_not_kill_the_scheduler(make_container):
    Broken.attempts = 0
    make_container(sys.modules[__name__])
    assert _wait_for(lambda: Broken.attempts >= 2)


def test_cron_jobs_are_registered(make_container):
    container = make_container(sys.modules[__name__])
    registrar = container.get(SchedulerRegistrar)
    job_ids = [j.id for j in registrar._scheduler.get_jobs()]
    assert any(job_id.endswith("Nightly.rollup") for job_id in job_ids)


def test_disabled_setting_skips_scheduler(make_container):
    container = make_container(sys.modules[__name__], config={"scheduling": {"enabled": False}})
    assert container.get(SchedulerRegistrar)._scheduler is None


def test_no_scheduled_methods_no_scheduler(make_container):
    container = make_container()
    assert container.get(SchedulerRegistrar)._scheduler is None


def test_scheduled_requires_exactly_one_trigger():
    with pytest.raises(ValueError, match="exactly one"):
        scheduled()
    with pytest.raises(ValueError, match="exactly one"):
        scheduled(every=1, cron="* * * * *")


def test_scheduled_rejects_non_positive_interval():
    with pytest.raises(ValueError, match="positive"):
        scheduled(every=0)
