import pytest

import capybara


class Driver(object):
    def __init__(self, name, skip=None):
        self.name = name
        self.skip = skip or []


@pytest.fixture(
    scope="session",
    params=[
        Driver("selenium"),
        Driver("werkzeug", skip=[
            "frames", "hover", "js", "modals", "screenshot", "send_keys", "server", "windows"])],
    ids=lambda d: d.name)
def driver(request):
    return request.param


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    requires = item.get_marker("requires")
    if requires is not None:
        driver = item.callspec.params.get("driver")

        skipped_features = set(driver.skip)
        required_features = set(requires.args)

        missing_features = required_features & skipped_features
        if missing_features:
            pytest.skip("test requires {}".format(", ".join(sorted(list(missing_features)))))


@pytest.fixture(autouse=True)
def setup_capybara():
    original_default_selector = capybara.default_selector
    try:
        capybara.default_selector = "xpath"
        yield
    finally:
        capybara.default_selector = original_default_selector
