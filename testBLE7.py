import asyncio
from bleak import BleakScanner
from bleak import BleakClient

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


# Connect to the target Penguin with sepecific MAC address
# format of the input mac address is "XX:XX:XX:XX:XX:XX"
async def connect_Penguin(address):
    # Discover nearby Bluetooth devices
    devices = await BleakScanner.discover()

    # Loop through each device and print detailed information
    for device in devices:
        if device.name is not None and "Penguin" in device.name:
            manu_data = device.metadata.get('manufacturer_data', 'N/A')
            manu_data = manu_data.get(2504, 'N/A')
            if manu_data != 'N/A':
                mac_hex = manu_data[0:6].hex()
                formatted_mac = ':'.join(mac_hex[i:i+2] for i in range(0, len(mac_hex), 2))
                if formatted_mac == address or formatted_mac != address:
                    # found the target Penguin

                    print(f"Device Name: {device.name}")
                    print(f"MAC Address: {device.address}")
                    print(f"RSSI (Signal Strength): {device.rssi} dBm")
                    print(f"Manufacturer Data: {device.metadata.get('manufacturer_data', 'N/A')}")
                    print(f"MAC: {formatted_mac}")
                    print(f"PN: {manu_data[10:]}")
                    print(f"Service UUIDs: {device.metadata.get('uuids', 'N/A')}")
                    print(f"TX Power: {device.metadata.get('tx_power', 'N/A')}")
                    print('-' * 50)

                    if device.rssi < -66:
                        continue
                    
                    # get the MAC address of the target Penguin
                    mac_address = device.address
                    # connect to the target Penguin
                    async with BleakClient(mac_address) as client:
                        # print the client address
                        print(f"MAC Address: {client.address}")
                        
                        # get the services of the target Penguin
                        services = await client.get_services()
                        for service in services:
                            print(f"service: {service}")

                            for char in service.characteristics:
                                print(f"  Characteristic: {char.uuid} (Handle: {char.handle}) - {char.properties}")

                                # Example: Read characteristics that are readable
                                if "read" in char.properties:
                                    try:
                                        value = await client.read_gatt_char(char.uuid)
                                        print(f"    Value: {value} | Hex value: {value.hex()}")
                                        
                                    except Exception as e:
                                        print(f"    Failed to read characteristic: {e}")
                            print('+' * 50)
                        
                    # Device will disconnect when block exits.
                            
 
                    # break

# Run the scanner
# asyncio.run(scan())
# asyncio.run(connect_Penguin("e3:c0:42:d1:05:27"))
asyncio.run(connect_Penguin("f4:e7:24:45:42:b1"))
