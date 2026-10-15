import asyncio
import time

from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        api = await p.request.new_context(base_url = "https://jsonplaceholder.typicode.com")

        response = await api.get("/posts/1")
        assert response.status == 200

        body = await response.json()

        assert body["id"] == 1

        print("Status :", response.status, "| Title :", body["title"])

        created = await api.post("/posts" , data = {"title":"qa","body":"async","userId":1})


        start = time.perf_counter()
        responses = await asyncio.gather(*(api.get(f"/posts/{i}") for i in range(1,11)))
        assert all(r.ok for r in responses)

        print("Created :", created.status, await created.json())
        print(f"{len(responses)} posts fetched in {time.perf_counter() - start:.2f}s")


        await api.dispose()

asyncio.run(main())

