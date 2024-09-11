# --------------------------------------------------
# Device Name: Penguin-4081601747
# MAC Address: 3138E289-055E-4BE5-97AA-966B1B2476D5
# RSSI (Signal Strength): -50 dBm
# Manufacturer Data: {2504: b"\xe3\xc0B\xd1\x05' @P*TN72024081601747"}
# Service UUIDs: []
# TX Power: N/A

# Define the byte sequence
# byte_sequence = b"\xe3\xc0B\xd1\x05'"
byte_sequence = b"\xe3\xc0B\xd1\x05' @P*TN72024081601747"
# Split the byte sequence based on the space (which is ASCII 0x20)
parts = byte_sequence.split(b' ')

# Convert the two parts back into a readable format
first_part = parts[0].hex()  # This will give the first part in hexadecimal format
# second_part = parts[1].hex()  # The second part seems to be readable ASCII
second_part = parts[1].decode('utf-8', errors='ignore')  # The second part seems to be readable ASCII

# Print the results
print(f"MAC: {first_part}")
print(f"PN: {second_part}")

# # Print the result
# print(hex_representation)
