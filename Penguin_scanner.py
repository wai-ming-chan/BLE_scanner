import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import datetime

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Connect to the target Penguin with sepecific MAC address
# format of the input mac address is "XX:XX:XX:XX:XX:XX"
async def connect_Penguin(address):

    # output variables
    op_device_name = ""
    op_mac_addr = ""
    op_RSSI = ""
    op_address = ""
    op_PN = ""
    op_b_level = ""
    op_temp = ""

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
                if formatted_mac == address:
                    # found the target Penguin

                    print(f"Device Name: {device.name}")
                    print(f"MAC Address: {device.address}")
                    print(f"RSSI (Signal Strength): {device.rssi} dBm")
                    # print(f"Manufacturer Data: {device.metadata.get('manufacturer_data', 'N/A')}")
                    print(f"MAC: {formatted_mac}")
                    PN_data = manu_data[10:]
                    PN_data = PN_data.decode('utf-8')
                    print(f"PN: {PN_data}")
                    # print(f"Service UUIDs: {device.metadata.get('uuids', 'N/A')}")
                    # print(f"TX Power: {device.metadata.get('tx_power', 'N/A')}")
                    
                    op_device_name = device.name
                    op_mac_addr = formatted_mac
                    op_RSSI = device.rssi
                    op_address = device.address
                    op_PN = manu_data[10:]

                    # print('-' * 50)

                    if device.rssi < -70:
                        continue
                    
                    # get the MAC address of the target Penguin
                    mac_address = device.address
                    # connect to the target Penguin
                    async with BleakClient(mac_address) as client:
                        
                        # print(f">>>> MAC Address: {client.address}") # print the client address
                        # print(f"Connected: {client.is_connected}") # check if the Penguin is connected

                        # get the services of the target Penguin
                        services = await client.get_services()
                        for service in services:
                            # print(f"service: {service}")

                            for char in service.characteristics:
                                # print(f"  characteristic: {char.uuid} (Handle: {char.handle}) - {char.properties}")

                                # Example: Read characteristics that are readable
                                if "read" in char.properties:
                                    try:
                                        value = await client.read_gatt_char(char.uuid)
                                        
                                        if "Battery Level" in str(char):
                                            op_b_level = value[0]
                                            print(f'SoC: {op_b_level}%')
                                            # print(f"    Value: {op_b_level}")
                                        elif "Temperature" in str(char):
                                            op_temp = value[0]
                                            print(f'Temperature: {op_temp}F')
                                        else:
                                            # print(f"    Value: {value} | Hex value: {value.hex()}")
                                            pass 
                                    except Exception as e:
                                        # print(f"    Failed to read characteristic: {e}")
                                        pass
                            # print('+' * 50)
                    # Device will disconnect when block exits.
                    # returnSTR = f"{datetime.datetime.now().strftime('%Y-%m-%d,%H:%M:%S')},{PN_str},{formatted_mac},{b_level},{args.address}\n"
                    print('-' * 50)
                    # return {formatted_mac, PN_data, op_b_level, op_temp}
                    return formatted_mac, PN_data, op_b_level, op_temp
                    # return {datetime.datetime.now().strftime('%Y-%m-%d,%H:%M:%S'), op_device_name,op_mac_addr,op_RSSI,op_address,op_PN,op_b_level}
    return False


def run_scanner(input_address):
    # Run the scanner
    flag_success = asyncio.run(connect_Penguin(input_address))

    print(f'Founded? {flag_success}')
    return flag_success
