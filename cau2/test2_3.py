from test1_1 import data, lines

# Let's verify if "BlueTeam" is the correct key
# by decrypting the first line

full_key = "BlueTeam"
first_line_hex = lines[0]

# Decrypt first 50 characters
cipher_bytes = bytes.fromhex(first_line_hex[:100])  # First 50 bytes
key_bytes = full_key.encode('utf-8')

decrypted = []
for i in range(len(cipher_bytes)):
    decrypted_byte = cipher_bytes[i] ^ key_bytes[i % len(key_bytes)]
    decrypted.append(decrypted_byte)

plaintext = bytes(decrypted).decode('utf-8', errors='ignore')
print(f"Key: '{full_key}'")
print(f"First 50 chars decrypted: '{plaintext}'")
print("\nDoes this look like English? If yes, we found the key!")