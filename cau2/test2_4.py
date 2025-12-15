from test1_1 import data, lines

# Find a line starting with 00000000
null_line = lines[1]  # Line 2
print(f"Line with null bytes: {null_line[:40]}...")

# Extract the null bytes and following bytes
null_count = 0
for i in range(0, len(null_line), 2):
    if null_line[i:i+2] == "00":
        null_count += 1
    else:
        break

print(f"\nFirst {null_count} bytes are 0x00")
print("This means: Plaintext = Key at these positions")
print(f"Or: The plaintext starts with {null_count} null bytes")

# Look at bytes after the nulls
after_nulls_hex = null_line[null_count*2:null_count*2+16]
after_nulls_bytes = bytes.fromhex(after_nulls_hex)
print(f"\nBytes after nulls: {after_nulls_hex}")
print(f"As integers: {[f'0x{b:02x}' for b in after_nulls_bytes]}")