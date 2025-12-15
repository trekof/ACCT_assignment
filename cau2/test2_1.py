# Test if 16041045 decrypts to "The "
cipher_hex = "16041045"
guess = "The "

# Convert hex to bytes
cipher_bytes = bytes.fromhex(cipher_hex)

# XOR to find key
key_bytes = []
for i in range(4):
    key_byte = cipher_bytes[i] ^ ord(guess[i])
    key_bytes.append(key_byte)
    print(f"Byte {i+1}: 0x{cipher_bytes[i]:02x} XOR '{guess[i]}' (0x{ord(guess[i]):02x}) = 0x{key_byte:02x} ('{chr(key_byte)}')")

key_fragment = ''.join(chr(b) for b in key_bytes)
print(f"\nKey fragment found: '{key_fragment}'")