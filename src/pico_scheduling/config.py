"""Settings for pico-scheduling (prefix ``scheduling``, zero-config)."""

from dataclasses import dataclass

from pico_ioc import configured


@configured(target="self", prefix="scheduling", mapping="tree")
@dataclass
class SchedulingSettings:
    """``enabled: false`` disables every ``@scheduled`` job."""

    enabled: bool = True
