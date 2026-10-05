import asyncio
import time

async def fake_request(name:str,delay:float):
    await asyncio.sleep(delay)
    return f"{name} done in {delay}s"


async def sequential():
    return [await fake_request(f"req{i}",1) for i in range (10)]

async def concurrent():
    return await asyncio.gather(*[fake_request(f"req{i}",1)
                                   for i in range(10)])


async def timed(label,coro):
    start = time.perf_counter()
    result = await coro
    print(f"{label}: {result} in {time.perf_counter() - start:.2f}s")



async def main():
    await timed ("sequential",sequential())
    await timed ("concurrent",concurrent())

asyncio.run(main())
