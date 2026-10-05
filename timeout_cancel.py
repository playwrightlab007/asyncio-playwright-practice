
import asyncio

async def slow_load_state(delay):
    try:
        await asyncio.sleep(delay)
        print("Page loaded successfully")
        return "SUCCESS"

    except asyncio.CancelledError:
        print("Clean up : Page load cancelled")
        raise

    finally:
        print("Cleanup always runs")


async def main():

    task = asyncio.create_task(slow_load_state(0.3))

    try:
        async with asyncio.timeout(6):
            await task
            

    except TimeoutError:
        print("Timeout after 1s")

    else: 
        print("Page loaded in time")


asyncio.run(main())