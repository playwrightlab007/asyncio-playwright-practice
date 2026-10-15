import asyncio
import json

from playwright.async_api import async_playwright , Route

async def fake_products(route:Route):

    await route.fulfill(status = 200,content_type="application/json",
                        body = json.dumps([{"id":1,"title":"Mocked Item"}]),)



async def main():
    async with async_playwright() as p:

        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.route("**/api/products" , fake_products)
        await page.goto("https://example.com")

        data = await page.evaluate("fetch('/api/products').then(r => r.json())")

        assert data[0]["title"] == "Mocked Item"
        print("Mocked response is :" , data)

        await browser.close()

asyncio.run(main())
