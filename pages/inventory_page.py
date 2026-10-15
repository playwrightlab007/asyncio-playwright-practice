import re
from playwright.async_api import Page, expect
from pages.base_page import Base_page

class InventoryPage(Base_page):
    path = "/inventory.html"

    def __init__(self, page:Page):
        super().__init__(page)
        self.items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")


    async def expect_loaded(self):
        await expect(self.page).to_have_url(re.compile("inventory"))
        await expect(self.items).not_to_have_count(0)

    async def add_to_cart(self , product_slug):
        await self.page.locator(f'[data-test="add-to-cart-{product_slug}"]').click()

        
