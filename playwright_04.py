import asyncio
import time

from playwright.async_api import async_playwright , Browser

URLs = ["https://playwright.dev",
    "https://example.com",
    "https://www.saucedemo.com",]

MORE_URLs = ["https://www.python.org",
    "https://docs.python.org/3/",
    "https://pypi.org",
    "https://www.wikipedia.org",
    "https://developer.mozilla.org",
    "https://news.ycombinator.com",
    "https://quotes.toscrape.com",
    "https://books.toscrape.com",
    "https://httpbin.org/html",
    "https://example.org",]


async def get_title(browser:Browser , url:str , sem:asyncio.Semaphore | None = None):
    if sem is None:
        sem = asyncio.Semaphore(1)        # no limit given: just use a private one

    async with sem:
        context = await browser.new_context()
        try:
            page = await context.new_page()
            await page.goto(url , timeout=30_000)
            return url , await page.title()
        finally:
            await context.close()


def show(results):
    for url, r in results:
        title = f"FAILED: {type(r).__name__}" if isinstance(r, Exception) else r
        print(f"   {url:<32} {title}")


async def safe(coro, url):
    # keep the url next to an error so one bad site doesn't hide the others
    try:
        return await coro
    except Exception as e:
        return url , e


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # 1) the same three sites, one after another
        start = time.perf_counter()
        results = [await safe(get_title(browser , u), u) for u in URLs]
        seq = time.perf_counter() - start
        print(f"Sequential : {len(URLs)} sites in {seq:.1f}s")
        show(results)

        # 2) the same three sites, all at once
        start = time.perf_counter()
        results = await asyncio.gather(*(safe(get_title(browser , u), u) for u in URLs))
        con = time.perf_counter() - start
        print(f"Concurrent : {len(URLs)} sites in {con:.1f}s  ({seq/con:.1f}x faster)")
        show(results)

        # 3) thirteen sites, at most 4 open at a time
        all_urls = URLs + MORE_URLs
        sem = asyncio.Semaphore(4)
        start = time.perf_counter()
        results = await asyncio.gather(*(safe(get_title(browser , u , sem), u) for u in all_urls))
        print(f"Semaphore(4): {len(all_urls)} sites in {time.perf_counter() - start:.1f}s")
        show(results)

        await browser.close()

asyncio.run(main())
