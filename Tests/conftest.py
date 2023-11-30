import pytest
from _pytest.config import hookimpl
from selenium import webdriver

from Library.configure import Configuration


@pytest.fixture(params=["chrome"])
def init_driver(request):
    global driver
    browser = request.param

    if browser.lower() == "chrome":
        driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(Configuration.URL)
    yield driver
    driver.close()


# function captures screenshot
def _capture_screenshot():
    return driver.get_screenshot_as_base64()


@hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        xfail = hasattr(report, "wasfail")
        # if report: # attaches screenshots for all steps
        if (report.skipped and report.fail) or (report.failed and not xfail):
            # only add additional html on failure
            extra.append(pytest_html.extras.image(_capture_screenshot()))
        report.extra = extra


