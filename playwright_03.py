import asyncio
import time

from playwright.async_api import async_playwright , expect , Browser

URLs = ["https://playwright.dev",
    "https://example.com",
    "https://www.saucedemo.com",]


async def get_title(browser:Browser , url:str):
    context = await browser.new_context()
    try:

        page = await context.new_page()
        await page.goto(url)
        return url , await page.title()
    finally:
        await context.close()


async def main():
    async with async_playwright() as p:
         browser = await p.chromium.launch()

         start = time.perf_counter()
         results = await asyncio.gather(*(get_title(browser , u) for u in URLs))

         print(f"{len(URLs)} sites in {time.perf_counter() -start:.1f}s")

         for url, title in results:
             print(f"{url:<32} {title}")

            
    await browser.close()

asyncio.run(main())




