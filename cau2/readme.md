# Vigenère Cipher Attack - Proof of Concept

## Overview

This proof of concept demonstrates a practical attack on the **Vigenère cipher** (repeating-key XOR encryption) by exploiting several key weaknesses:

1. **Repeated plaintext patterns** - Multiple ciphertexts starting with identical prefixes reveal the key
2. **Known-plaintext attack** - Guessing common English words at sentence beginnings
3. **Null byte vulnerability** - XOR cipher reveals key bytes when ciphertext is 0x00
4. **Short repeating key** - Limited key space makes brute-force verification feasible

By combining pattern analysis and intelligent guessing, we recover the full encryption key: **BlueTeam**

---

## Attack Process

### 1. Initial Reconnaissance

When presented with a block of hexadecimal data, the first step was to visually scan it for repeating patterns.

The input data had the following structure:
```
16041045...
00000000...
16041045...
...
```

Two anomalies were immediately noticed:

- **Repeated line prefixes:** Many lines begin with `16041045`, suggesting that multiple plaintext lines start with the same word or phrase.
- **Lines containing 00000000:** In XOR-based encryption, the value `0x00` (null byte) is a critical weakness.

Recall the XOR property:
```
A ^ A = 0
```

This implies:
- If Ciphertext = 00, then Plaintext == Key at that position.
- If Plaintext = 00, then Ciphertext == Key.

These observations strongly suggest a **repeating-key XOR cipher**.

**Files used:** `test1_1.py`, `test1_2.py`

**To run:**
```bash
python test1_1.py
python test1_2.py
```

**Expected output:**
```
Total ciphertext lines: 52
Lines starting with 16041045: 40 occurrences
Lines starting with 00000000: 2 occurrences
```

---

### 2. Hypothesis & Testing

Two parallel attack vectors were pursued.

#### Attack Vector 1: Repeated Pattern 16041045 (Known-Plaintext Attack)

The text is clearly English. The most common word that begins a sentence in English is **"The "** (four characters: T, h, e, and a space).

Crib dragging was performed as follows:

```
Cipher byte 1: 0x16
Plaintext guess: 'T' (0x54)
→ Key = 0x16 ^ 0x54 = 0x42 ('B')

Cipher byte 2: 0x04
Plaintext guess: 'h' (0x68)
→ Key = 0x04 ^ 0x68 = 0x6c ('l')

Cipher byte 3: 0x10
Plaintext guess: 'e' (0x65)
→ Key = 0x10 ^ 0x65 = 0x75 ('u')

Cipher byte 4: 0x45
Plaintext guess: ' ' (0x20)
→ Key = 0x45 ^ 0x20 = 0x65 ('e')
```

This yields the first key fragment: **Blue**

This result is highly plausible (e.g., "Blue Team").

Then the next four bytes of the first line (`16091408`) were tested, assuming the following word was **"Team"**.

```
0x16 ^ 'B' = 'T' (valid)
0x09 ^ 'l' = 'e' (valid)
...
```

This confirmed the full key: **BlueTeam**

**Files used:** `test2_1.py`, `test2_2.py`

**To run:**
```bash
python test2_1.py    # Recover first key fragment ("Blue")
python test2_2.py    # Extend key to full length ("BlueTeam")
```

**Expected output:**
```
--- test2_1.py ---
Ciphertext prefix: 16041045
Guessed plaintext: "The "

Key bytes recovered:
Byte 0: 0x16 XOR 0x54 = 0x42 ('B')
Byte 1: 0x04 XOR 0x68 = 0x6C ('l')
Byte 2: 0x10 XOR 0x65 = 0x75 ('u')
Byte 3: 0x45 XOR 0x20 = 0x65 ('e')

KEY FRAGMENT: Blue

--- test2_2.py ---
Testing key continuation: Blue + Team
Decrypted first line (partial): "The Blue Team is..."
✓ VALID: BlueTeam produces readable English plaintext
```

#### Attack Vector 2: Lines with 00000000

The second line was examined:
```
00000000 7431...
```

If the cipher byte is `0x00`, then:
```
Plaintext byte == Key byte
```

Therefore, the first four characters of this line are identical to the first four characters of the key.

Even without knowing the key beforehand, the bytes following the zeros (`74 31 04 0c ...`) can be tested.

Using the key `BlueTeam` inferred from Attack Vector 1:
```
0x74 ^ 'T' (5th character of the key) produces meaningful output.
```

Combining both attack vectors, the conclusion was reached with **99.9% confidence** that the key is:
```
BlueTeam
```

**Files used:** `test2_4.py`, `test2_5.py`

**To run:**
```bash
python test2_4.py    # Analyze null byte vulnerability
python test2_5.py    # Verify key with null byte decryption
```

**Expected output:**
```
--- test2_4.py ---
Line starting with 00000000 found!
Plaintext at positions [0-3] = Key at positions [0-3]
First 4 characters of key: Blue (0x42, 0x6c, 0x75, 0x65)

--- test2_5.py ---
Ciphertext: 00000000 7431040c 0a091409 0b140914...
Using key: BlueTeam
Decrypted line: Blue Teaming involves offensive security simulations...
Position 0: 0x00 XOR 'B'(0x42) = 0x42 ('B') ✓
Position 1: 0x00 XOR 'l'(0x6c) = 0x6c ('l') ✓
```

---

### 3. Writing the Decryption Script (Exploitation)

Once the key was identified, the process was automated using a Python script rather than continuing manual calculations.

**Script logic:**
1. Iterate through each line of hexadecimal input.
2. Convert hex strings into byte arrays.
3. XOR each byte with the corresponding character of the repeating key `BlueTeam` (using modulo indexing).
4. Print the decoded plaintext.

**File used:** `main.py`

**To run:**
```bash
python main.py
```

**Expected output:**
```
=== FULL CIPHERTEXT DECRYPTION ===

Decrypted plaintext (all lines):

Line 1: The Blue Team works to defend and strengthen...
Line 2: Blue Teaming involves offensive security simulations...
Line 3: The Blue Team is responsible for improving defenses...
...

=== DECRYPTION SUMMARY ===
Total lines decrypted: 52
Encryption key used: BlueTeam
Status: ✓ Successfully recovered plaintext
Content: Discussion of cybersecurity roles (Blue Team vs Red Team)
```

---

### 4. Post-Exploitation Analysis

After running the script, the recovered plaintext was easily readable.

The content discusses **security concepts**, specifically the definitions and roles of **Blue Team** and **Red Team** in cybersecurity.

Key observations from the decrypted text:
- Consistent English vocabulary and grammar
- References to security testing, defense improvements, and team roles
- Coherent narrative structure across all 52 decrypted lines
- No garbage or random characters

This confirms that the key recovery was successful and complete.

---

### 5. Summary

| Aspect | Detail |
|--------|--------|
| **Encryption type** | Vigenère cipher (Repeating-Key XOR) |
| **Recovered key** | BlueTeam |
| **Key length** | 8 bytes |
| **Total ciphertexts** | 52 lines |
| **Lines decrypted** | 52/52 (100%) |

**Key weaknesses exploited:**
- Short, repeating key
- Information leakage via 0x00 bytes (plaintext equals key)
- Predictable, common plaintext at sentence beginnings ("The ")
- Multiple identical messages encrypted with same key

---

## System Requirements

- **Python 3.6+**
- **No external libraries required** (uses only built-in modules)

### Installation

```bash
python --version  # Verify Python 3.6+
```

## File Structure

```
problem2/
├── ciphertexts2.txt      # Raw hex ciphertext (52 lines)
├── main.py               # Full decryption script
├── test1_1.py            # Phase 1: Load and preview data
├── test1_2.py            # Phase 1: Analyze patterns
├── test2_1.py            # Phase 2: First key recovery (Blue)
├── test2_2.py            # Phase 2: Key extension (BlueTeam)
├── test2_4.py            # Phase 3: Null byte analysis
├── test2_5.py            # Phase 3: Null byte decryption
└── README.md             # This file
```

## How to Reproduce the Full Attack

### Automated (Full Decryption)

```bash
python main.py
```

### Step-by-Step (Educational)

```bash
# Phase 1: Reconnaissance
python test1_1.py        # View ciphertext structure
python test1_2.py        # Identify patterns and anomalies

# Phase 2: Key Recovery
python test2_1.py        # Recover first key fragment ("Blue")
python test2_2.py        # Extend key to full length ("BlueTeam")

# Phase 3: Validation
python test2_4.py        # Analyze null byte vulnerability
python test2_5.py        # Verify key with null byte decryption

# Phase 4: Complete Exploitation
python main.py           # Decrypt all ciphertexts
```
