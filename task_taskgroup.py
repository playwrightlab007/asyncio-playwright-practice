import asyncio

async def worker(name:str,delay:float):
    await asyncio.sleep(delay)

    if name == "search":
        raise Exception("Search is failed")
    
    print(f"{name} is finished")
    return name.upper()


async def main():
    login = asyncio.create_task(worker("login", 0.3))
    print("Task is scheduled,doing the other work")
    await asyncio.sleep(0.1)
    print("result : " , await login)

    try:
        async with asyncio.TaskGroup() as tg:
            search = tg.create_task(worker("search",0.2))
            checkout = tg.create_task(worker("checkout",0.5))
            login = tg.create_task(worker("login",1.0))

    except Exception as e:
        print("Something is wrong:" , e)


    else:

        print("Both completed :", login.result() ,search.result() , checkout.result())


    # result = await asyncio.gather(worker("login", 0.5),
    #                               worker("search", 0.2),
    #                               worker("checkout",0.1))



asyncio.run(main())