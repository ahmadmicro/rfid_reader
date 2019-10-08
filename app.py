import asyncio
import serial
from reader import Reader
from datapoint import DataPoint

cardreader = Reader('COM3')
async def doer():
    datas = []
    await asyncio.sleep(2)
    print('starting')
    card = await cardreader.getSerial()
    print(card)
    try:
        lastblock = await cardreader.read(0)
        lastblock = int(lastblock)
        print(lastblock)
        for block in range(lastblock):
            try:
                data = DataPoint(card, await cardreader.read(block))
                print(data)
                if data.date:
                    datas.append(data)
            except Exception as ex:
                print(ex)
        cardreader.running  = False
    except:
        print('please place a card on the reader')
    print(datas)
    quit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    tasks = [
        loop.create_task(cardreader.wait()),
        loop.create_task(doer())
    ]

    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)