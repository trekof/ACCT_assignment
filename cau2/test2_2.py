# We have "Blue" - what comes next?
# Let's test a few possibilities

known_key = "Blue"
next_cipher_hex = "16091408"
next_cipher_bytes = bytes.fromhex(next_cipher_hex)

guesses = ["Team", "Flag", "Code", "Secu"]

print("Testing different guesses for next 4 bytes:")
for guess in guesses:
    key_bytes = []
    for i in range(4):
        key_byte = next_cipher_bytes[i] ^ ord(guess[i])
        key_bytes.append(key_byte)
    
    key_fragment = ''.join(chr(b) for b in key_bytes)
    
    # Check if it matches our known key pattern
    full_key = known_key + key_fragment
    print(f"\nGuess: '{guess}' -> Key becomes: '{full_key}'")
    
    # Check if first 4 bytes match
    matches = all(key_bytes[i] == ord(known_key[i]) for i in range(4))
    if matches:
        print(f"  -> MATCH! This continues our key pattern!")
    else:
        print(f"  -> No match. Expected 'Blue' pattern to repeat.")