import pytest
from pico_ioc import DictSource, configuration, init


@pytest.fixture(autouse=True)
def isolate_from_installed_plugins(monkeypatch):
    monkeypatch.setenv("PICO_BOOT_AUTO_PLUGINS", "false")


@pytest.fixture
def make_container():
    created = []

    def _make(*modules, config=None):
        cfg = configuration(DictSource(config or {}))
        container = init(modules=["pico_scheduling", *modules], config=cfg)
        created.append(container)
        return container

    yield _make
    for c in reversed(created):
        c.shutdown()
