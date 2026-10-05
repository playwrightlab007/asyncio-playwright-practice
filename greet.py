import asyncio

async def greet(name:str)->str:
    await asyncio.sleep(0.1)
    return f"Hello!!! {name}"

async def main():
    message = await greet("Saurabh Singh")
    print(message)


asyncio.run(main())