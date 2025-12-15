# Read the ciphertext file
with open('ciphertexts2.txt', 'r') as f:
    data = f.read()

# Split into lines
lines = data.strip().split('\n')
print(f"Total lines: {len(lines)}")
print("\nFirst 10 lines (showing first 50 chars each):")
for i in range(10):
    print(f"Line {i+1:2d}: {lines[i][:50]}...")