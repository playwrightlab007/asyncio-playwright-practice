import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def fake_session(name:str):
    print(f"{name} open")
    try:
        yield name

    finally:
        await asyncio.sleep(0.3)
        print(f"{name} close")

async def paged_results(page:int):
    for p in range(1 , page+1):
        await asyncio.sleep(0.1)
        yield [f"item {p}-{i}" for i in range(10)]


async def main():
    async with fake_session("browser") as session:
        async for batch in paged_results(4):
            print(session,batch)


asyncio.run(main())