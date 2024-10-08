import asyncio
from bleak import BleakScanner

async def scan():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)
        print(device.name)
        print(device.address)
        print(device.details)
        print('-' * 50)

# Run the scanner
asyncio.run(scan())

