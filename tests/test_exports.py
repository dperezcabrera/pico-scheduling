"""The public API is exactly what ``__all__`` declares (stability contract)."""

import pico_scheduling


def test_public_api_is_declared_and_importable():
    assert set(pico_scheduling.__all__) == {"SchedulerRegistrar", "SchedulingSettings", "scheduled"}
    for name in pico_scheduling.__all__:
        assert getattr(pico_scheduling, name) is not None
