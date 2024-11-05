import asyncio


async def wait(time: float):
    while True:
        await asyncio.sleep(time)
        print(f"Waited for {time} seconds.")


async def main():
    task = [
        asyncio.create_task(wait(1)),
        asyncio.create_task(wait(2)),
        asyncio.create_task(wait(3)),
    ]

    await asyncio.gather(*task)


asyncio.run(main())
