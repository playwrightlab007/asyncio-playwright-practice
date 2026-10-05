
import asyncio
import time 

def blocking_read_report():
    time.sleep(1)
    return "report parsed"

async def heartbeat():
    for _ in range(4):
        print("Event loop is running")
        await asyncio.sleep(0.3)


async def main ():
    results = await asyncio.gather(asyncio.to_thread(blocking_read_report) , heartbeat())
    print(results)


asyncio.run(main())