import asyncio
import time

async def myAsyncFunc():
    print("Started async fun")
    return 20

async def min():
    print(f"started at {time.strftime('%X')}")

    say_after(1, 'hello')
    # say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


asyncio.run(min())