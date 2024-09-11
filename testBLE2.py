import asyncio
from bleak import BleakClient

# address = "e3:c0:42:d1:05:27"
address = "73F9467E-0917-7567-45FD-28796115945A"
MODEL_NBR_UUID = "2A24"

async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main(address))