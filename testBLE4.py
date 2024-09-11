import asyncio
from bleak import BleakScanner

async def scan():
    print(f"{'Device Name':<25} {'MAC Address':<20} {'RSSI (dBm)':<10} {'UUIDs/Services'}")
    print("="*80)
    
    devices = await BleakScanner.discover()
    for device in devices:
        # Get the device name
        device_name = device.name or "Unknown"
        
        # Get the MAC address
        mac_address = device.address
        
        # Get RSSI (signal strength in dBm)
        rssi = device.rssi
        
        # Get advertised services (UUIDs) if available
        uuids = device.metadata.get("uuids", [])
        if not uuids:
            uuids = ["No UUIDs advertised"]
        
        # Print device information
        print(f"{device_name:<25} {mac_address:<20} {rssi:<10} {', '.join(uuids)}")

# Run the scanner
asyncio.run(scan())
