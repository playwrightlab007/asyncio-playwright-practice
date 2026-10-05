import asyncio

async def worker(name:str,queue:asyncio.Queue,results:list):

    while True:
        url = await queue.get()

        try:
            await asyncio.sleep(0.2)
            results.append((name,url,200))

        finally:
            queue.task_done()

async def main():
    queue:asyncio.Queue = asyncio.Queue()
    results :list =[]

    workers = [asyncio.create_task(worker(f"w{i}", queue , results)) 
               for i in range(5)]


    for i in range(10):
        await queue.put(f"/page/{i}")

    await queue.join()

    for w in workers:
        w.cancel()

    await asyncio.gather(*(workers),return_exceptions=True)

    print(f"{len(results)} pages checked by {len({r[0] for r in results })} workers")


asyncio.run(main())