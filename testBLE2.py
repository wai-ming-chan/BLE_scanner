"""
This Python script connects to a Bluetooth Low Energy (BLE) device using the Bleak library.
It uses the device's UUID to establish a connection and retrieves the model number by reading a specific GATT characteristic.
The characteristic used to read the model number is identified by the predefined UUID "2A24" (commonly associated with model numbers in BLE devices).
Once the model number is retrieved, it is decoded and printed in a human-readable format.
"""

import asyncio
from bleak import BleakClient

# UUID = "e3:c0:42:d1:05:27"
# UUID = "73F9467E-0917-7567-45FD-28796115945A"
UUID = "257D64C3-28F3-8920-F7C5-36CA6F00D0D6"
MODEL_NBR_UUID = "2A24"

async def main(UUID):
    async with BleakClient(UUID) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main(UUID))