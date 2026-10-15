import re
import httpx
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

from config_utils import APPs , ARTIFACTS_DIR , BROWSER , HEADLESS, AppConfig
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

def pytest_addoption(parser):
    parser.addoption("--app", default = "app_one" ,
                     choices = list(APPs) , help= "application under test")



@pytest.fixture(scope="session")
def app(request):
    return APPs[request.config.getoption("--app")]


@pytest.hookimpl(wrapper=True , tryfirst=True)
def pytest_runtest_makereport(item , call):
    report = yield
    setattr(item, f"rep_{report.when}" , report)
    return report

@pytest_asyncio.fixture(scope = "session")
async def browser():
    async with async_playwright() as pw :
        browser = await getattr(pw, BROWSER).launch(headless = HEADLESS)
        yield browser
        await browser.close()

@pytest_asyncio.fixture
async def context(browser,app,request):
    ctx = await browser.new_context(base_url=app.base_url)
    await ctx.tracing.start(screenshots = True , snapshots = True)
    yield ctx

    call_report = getattr(request.node, "rep_call", None)
    failed = bool(call_report and call_report.failed)
    trace_path = None
    if failed:
        ARTIFACTS_DIR.mkdir(exist_ok=True)
        trace_path = ARTIFACTS_DIR / f"{re.sub(r'[^A-Za-z0-9_.-]', '_', request.node.name)}.zip"
    await ctx.tracing.stop(path=trace_path) 
    await ctx.close()


@pytest_asyncio.fixture
async def page(context):
    return await context.new_page()


@pytest_asyncio.fixture
async def api(app):
    async with httpx.AsyncClient(base_url=app.api_url, timeout = 10) as client:
        yield client


@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)




