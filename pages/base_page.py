from playwright.async_api import Page

class Base_page:

    path = "/"

    def __init__(self,page:Page):
        self.page = page

    async def open(self):
        await self.page.goto(self.path)

    async def title(self):
        return await self.page.title()