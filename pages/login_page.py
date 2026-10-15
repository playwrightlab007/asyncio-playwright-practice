
from playwright.async_api import Page
from pages.base_page import Base_page

class LoginPage(Base_page):
    path = "/"

    def __init__(self, page:Page):
        super().__init__(page)
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.submit = page.get_by_role("button" , name = "Login")
        self.error = page.locator('[data-test="error"]')


    async def login(self , username , password):
        await self.username.fill(username)
        await self.password.fill(password)
        await self.submit.click()

