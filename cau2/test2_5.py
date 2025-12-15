from test1_1 import data, lines

# Use our found key "BlueTeam" to decrypt the null byte line
key = "BlueTeam"
null_line_hex = lines[1]

cipher_bytes = bytes.fromhex(null_line_hex)
key_bytes = key.encode('utf-8')

# Decrypt first 30 bytes
decrypted = []
for i in range(min(30, len(cipher_bytes))):
    decrypted_byte = cipher_bytes[i] ^ key_bytes[i % len(key_bytes)]
    decrypted.append(decrypted_byte)

plaintext = bytes(decrypted).decode('utf-8', errors='ignore')
print(f"Key: '{key}'")
print(f"Decrypted (first 30 chars): '{plaintext}'")

# Show byte-by-byte for first 8 bytes
print("\nByte-by-byte decryption:")
for i in range(8):
    c = cipher_bytes[i]
    k = key_bytes[i % len(key_bytes)]
    p = c ^ k
    print(f"Position {i}: 0x{c:02x} XOR 0x{k:02x} ('{chr(k)}') = 0x{p:02x} ('{chr(p) if 32 <= p < 127 else '?'}')")