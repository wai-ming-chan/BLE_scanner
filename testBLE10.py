"""
Service Explorer
----------------

An example showing how to access and print out the services, characteristics and
descriptors of a connected GATT server.

Created on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>

# [Service for Serial Number]: 00002a25-0000-1000-8000-00805f9b34fb
# [Service for Batter Level]: 0000180f-0000-1000-8000-00805f9b34fb
----------------
Example of how to run the script for a specific service:
    python testBLE10.py --services=0000180f-0000-1000-8000-00805f9b34fb --address=257D64C3-28F3-8920-F7C5-36CA6F00D0D6

Example of how to run the script for all services:
    python testBLE10.py --address=257D64C3-28F3-8920-F7C5-36CA6F00D0D6

"""

import argparse
import asyncio
import logging
import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from bleak import BleakClient, BleakScanner

logger = logging.getLogger(__name__)


async def main(args: argparse.Namespace):
    returnSTR = ""
    logger.info("starting scan...")

    if args.address:
        device = await BleakScanner.find_device_by_address(
            args.address, cb=dict(use_bdaddr=args.macos_use_bdaddr)
        )
        if device is None:
            logger.error("could not find device with address '%s'", args.address)
            return
    else:
        device = await BleakScanner.find_device_by_name(
            args.name, cb=dict(use_bdaddr=args.macos_use_bdaddr)
        )
        if device is None:
            logger.error("could not find device with name '%s'", args.name)
            return

    logger.info("connecting to device...")

    async with BleakClient(
        device,
        services=args.services,
    ) as client:
        logger.info("connected")

        for service in client.services:
            logger.info("[Service] %s", service)
            
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = await client.read_gatt_char(char.uuid)
                        value_to_int = value[0]
                        extra = f", Value[line54]: {value} | int: {value_to_int}"

                    except Exception as e:
                        # extra = f", Error: {e}"
                        # extra = f", Error: n/a"
                        continue
                else:
                    extra = ""

                if "write-without-response" in char.properties:
                    extra += f", Max write w/o rsp size: {char.max_write_without_response_size}"

                logger.info(
                    "  [Characteristic] %s (%s)%s",
                    char,
                    ",".join(char.properties),
                    extra,
                )

                # print the Battery Level (char containing "Battery Level")
                if "Battery Level" in str(char):
                    b_level = value_to_int
                    
                if "Serial Number String" in str(char):
                    SN_str = value

                


                for descriptor in char.descriptors:
                    try:
                        value = await client.read_gatt_descriptor(descriptor.handle)
                        logger.info("    [Descriptor] %s, Value: %r", descriptor, value)
                    except Exception as e:
                        logger.error("    [Descriptor] %s, Error: %s", descriptor, e)
        # get device manufacturer data
        print(f"Manufacturer Data: {device.metadata.get('manufacturer_data', 'N/A')}")
        manu_data = device.metadata.get('manufacturer_data', 'N/A')
        manu_data = manu_data.get(2504, 'N/A')
        if manu_data != 'N/A':
            mac_hex = manu_data[0:6].hex()
            formatted_mac = ':'.join(mac_hex[i:i+2] for i in range(0, len(mac_hex), 2))
            print(f"MAC: {formatted_mac}")

            # print(f"MAC: {manu_data[4:10].hex()}")
            PN_str =manu_data[10:] 
            print(f"PN: {PN_str}")
            

        # return string [time],[address],[Battery Level] , time follows the format: yyyy-mm-dd,HH:MM:SS, address convert to hex and separated by ':', Battery Level is an integer
        returnSTR = f"{datetime.datetime.now().strftime('%Y-%m-%d,%H:%M:%S')},{PN_str},{formatted_mac},{b_level},{args.address}\n"
        print(returnSTR)

        logger.info("disconnecting...")

    logger.info("disconnected")
    
    saveFile = open("Penguin_records.csv", "a")
    saveFile.write(returnSTR)
    saveFile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    device_group = parser.add_mutually_exclusive_group(required=True)

    device_group.add_argument(
        "--name",
        metavar="<name>",
        help="the name of the bluetooth device to connect to",
    )
    device_group.add_argument(
        "--address",
        metavar="<address>",
        help="the address of the bluetooth device to connect to",
    )

    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )

    parser.add_argument(
        "--services",
        nargs="+",
        metavar="<uuid>",
        help="if provided, only enumerate matching service(s)",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="sets the log level to debug",
    )

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    asyncio.run(main(args))