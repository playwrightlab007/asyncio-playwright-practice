import asyncio
import re

from playwright.async_api import async_playwright , expect


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False , slow_mo=500)
        page = await browser.new_page()

        await page.goto("https://playwright.dev")
        await expect(page).to_have_title(re.compile("Playwright"))
        print("title :" , await page.title())

        await browser.close()


asyncio.run(main())