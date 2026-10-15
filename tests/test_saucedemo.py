from playwright.async_api import expect


async def test_login_shows_six_products(login_page , inventory_page , app):
    await login_page.open()
    await login_page.login(app.username , app.password)

    await inventory_page.expect_loaded()
    await expect(inventory_page.items).to_have_count(6)


async def test_wrong_password_shows_error(login_page , app):
    await login_page.open()
    await login_page.login(app.username , "wrong_password")

    await expect(login_page.error).to_contain_text("do not match")


async def test_add_to_cart_updates_badge(login_page , inventory_page , app):
    await login_page.open()
    await login_page.login(app.username , app.password)
    await inventory_page.expect_loaded()

    await inventory_page.add_to_cart("sauce-labs-backpack")

    await expect(inventory_page.cart_badge).to_have_text("1")


async def test_api_get_post(api):
    response = await api.get("/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
