import serial
import time
import asyncio
from datapoint import DataPoint

class Reader():
    def __init__(self, port='COM3'):
        self.ser = serial.Serial(port, 115200, timeout=0)
        self.running = True

    async def get_byte_async(self):
        while True:
            c = self.ser.read(1)
            if c == b'' :
                await asyncio.sleep(0)
            else:
                return c

    async def wait(self):
        val = bytearray()
        while self.running:
            b = await self.get_byte_async()
            if b!= b'\r' and b!=b'\n':
                if b!= b'\x00': val+=b
            elif len(val) != 0:
                self.val = val.decode('ascii')
                val = bytearray()

    async def _read(self):
        while True:
            await asyncio.sleep(1)
            if self.val != '':
                return self.val

    async def getSerial(self):
        self.ser.write("getserial:\n".encode('utf8'))
        return await self._read()

    async def read(self, address=0):
        self.ser.write(f"address:{address}\n".encode('utf8'))
        await self._read()
        self.ser.write("read:16\n".encode('utf8'))
        await self._read()
        if self.val == 'Address set': raise Exception(f'Error reading card at block {address}')
        if self.val == 'ERROR: SN': raise Exception('Error could not read card')
        return self.val

reader = Reader("COM3")
async def doer():
    datas = []
    await asyncio.sleep(2)
    print('starting')
    card = await reader.getSerial()
    print(card)
    try:
        lastblock = await reader.read(0)
        lastblock = int(lastblock)
        print(lastblock)
        for block in range(lastblock):
            try:
                data = DataPoint(card, await reader.read(block))
                print(data)
                if data.date:
                    datas.append(data)
            except Exception as ex:
                print(ex)
        reader.running  = False
    except:
        print('please place a card on the reader')
    print(datas)
    quit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    tasks = [
        loop.create_task(reader.wait()),
        loop.create_task(doer())
    ]

    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)

