import re 
import asyncio

from playwright.async_api import async_playwright , expect

async def main():
    async with async_playwright() as p:

        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("https://www.saucedemo.com")
        await page.get_by_placeholder("Username").fill("standard_user")
        await page.get_by_placeholder("Password").fill("secret_sauce")
        await page.get_by_role("button" , name="Login").click()

        await expect(page).to_have_url(re.compile("inventory"))
        await expect(page.locator(".inventory_item")).to_have_count(6)

        first_price = page.locator(".inventory_item_price").first
        print("First price :" , await first_price.inner_text())

        await browser.close()

asyncio.run(main())

