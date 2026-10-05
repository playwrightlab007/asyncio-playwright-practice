import asyncio
import time

async def call_api(i:int,sem: asyncio.Semaphore):
    async with sem:

        # print(f"{time.strftime('%X')} start{i}")
        print(f"start {i}")

        await asyncio.sleep(1)

        if i ==4 :
            raise Exception ("API 4 is failing")

        print(f"Finishes {i}")

        # print (f"{time.strftime("%X")} finshed{i}")

        return i

async def call_with_retry(i:int,sem:asyncio.Semaphore,retries:int=3):
    for attempt in range(1,retries+1):
        try:
            return await call_api(i,sem)
        except Exception as e:
            print(f"call{i} attempt {attempt}/{retries} failed :" , e)
            if attempt==retries:
                raise
            await asyncio.sleep(0.5)

async def main():
    sem = asyncio.Semaphore(3)

    start = time.perf_counter()
    results = await asyncio.gather(*(call_with_retry(i,sem) for i in range (9)),
                                   return_exceptions=True)
    
    end = time.perf_counter()

    print("Total time:" , end - start)
    print(results)


asyncio.run(main())