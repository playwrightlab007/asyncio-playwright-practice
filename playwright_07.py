import asyncio
from playwright.async_api import async_playwright , expect , Browser

AUTH_FILE = "auth.json"

async def login_and_save(browser : Browser):
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto("https://www.saucedemo.com")
    await page.get_by_placeholder("Username").fill("standard_user")
    await page.get_by_placeholder("Password").fill("secret_sauce")
    await page.get_by_role("button" , name="Login").click()
    await expect (page.locator(".inventory_item").first).to_be_visible()
    await context.storage_state(path=AUTH_FILE)
    await context.close()

async def open_inventory(browser : Browser,n : int):
    context = await browser.new_context(storage_state=AUTH_FILE)
    try:
        page = await context.new_page()
        await page.goto("https://www.saucedemo.com/inventory.html")
        await expect(page.locator(".inventory_item")).to_have_count(6)
        print(f"session {n}: Inventory loaded without logging in again")

    finally:
        await context.close()


async def main ():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        await login_and_save(browser)
        await asyncio.gather(*(open_inventory(browser , n) for n in range(1,10)))
        await browser.close()

asyncio.run(main())