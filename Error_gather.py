import asyncio

async def check(i:int):
    await asyncio.sleep(0.2 *(i+1))

    if i in (1, 3):
        raise ValueError(f"Check {i} --> 500 server not found")
    
    return f"check {i} ok --> 200"

async def main():

    results =await asyncio.gather(*(check(i) for i in range(4)),return_exceptions=True)

    for r in results :
        print("Fail :" if isinstance(r,Exception) else "Pass :" , r)


asyncio.run(main())