from test1_1 import data, lines

# Count lines starting with same prefix
from collections import Counter

# Check first 8 hex chars (4 bytes)
prefixes = [line[:8] for line in lines]
prefix_counts = Counter(prefixes)

print("Most common prefixes:")
for prefix, count in prefix_counts.most_common(5):
    print(f"  {prefix}: appears {count} times")

# Find lines starting with 00000000
null_lines = [i+1 for i, line in enumerate(lines) if line.startswith('00000000')]
print(f"\nLines starting with 00000000: {null_lines}")
print(f"Total: {len(null_lines)} lines")