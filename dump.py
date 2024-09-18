# Original string
uuid_string = "257D64C3-28F3-8920-F7C5-36CA6F00D0D6"

# Remove hyphens
clean_uuid = uuid_string.replace("-", "")

# Convert to hex
hex_value = hex(int(clean_uuid, 16))

# Output the hex value
print(hex_value)
