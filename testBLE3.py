import asyncio
from bleak import BleakScanner

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


async def scan():
    # Discover nearby Bluetooth devices
    devices = await BleakScanner.discover()

    # Loop through each device and print detailed information
    for device in devices:
            

        # If device name contains the word "Penguin"
        if device.name is not None and "Penguin" in device.name:
            if device.rssi < -66:
                continue
            print(f"Device Name: {device.name}")
            print(f"MAC Address: {device.address}")
            print(f"RSSI (Signal Strength): {device.rssi} dBm")
            print(f"Manufacturer Data: {device.metadata.get('manufacturer_data', 'N/A')}")
            manu_data = device.metadata.get('manufacturer_data', 'N/A')
            manu_data = manu_data.get(2504, 'N/A')
            if manu_data != 'N/A':
                mac_hex = manu_data[0:6].hex()
                formatted_mac = ':'.join(mac_hex[i:i+2] for i in range(0, len(mac_hex), 2))
                print(f"MAC: {formatted_mac}")

                # print(f"MAC: {manu_data[4:10].hex()}")
                print(f"PN: {manu_data[10:]}")
            print(f"Service UUIDs: {device.metadata.get('uuids', 'N/A')}")
            print(f"TX Power: {device.metadata.get('tx_power', 'N/A')}")
            print('-' * 50)

        # print(f"Device Name: {device.name or 'Unknown'}")
        # print(f"MAC Address: {device.address}")
        # print(f"RSSI (Signal Strength): {device.rssi} dBm")
        # print(f"Manufacturer Data: {device.metadata.get('manufacturer_data', 'N/A')}")
        # manu_data = device.metadata.get('manufacturer_data', 'N/A')

        # # if manu_data:
        # #     print(f"MAC: {manu_data[4:10].hex()}")
        # #     print(f"PN: {manu_data[10:]}")

        #     # Split the byte sequence based on the space (which is ASCII 0x20)
        # #     parts = manu_data.split(b' ')
        # #     # Convert the two parts back into a readable format
        # #     first_part = parts[0].hex()
        # #     second_part = parts[1].decode('utf-8', errors='ignore')
        # #     print(f"MAC: {first_part}")
        # #     print(f"PN: {second_part}")

        # print(f"Service UUIDs: {device.metadata.get('uuids', 'N/A')}")
        # print(f"TX Power: {device.metadata.get('tx_power', 'N/A')}")
        # print('-' * 50)

# Run the scanner
asyncio.run(scan())
