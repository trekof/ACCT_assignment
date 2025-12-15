1. Initial Reconnaissance
When presented with a block of hexadecimal data, my first step was to visually scan it for repeating patterns.
The input data had the following structure:
16041045...
00000000...
16041045...
...

I immediately noticed two anomalies:

- Repeated line prefixes: Many lines begin with 16041045, suggesting that multiple plaintext lines start with the same word or phrase.
- Lines containing 00000000: In XOR-based encryption, the value 0x00 (null byte) is a critical weakness.

Recall the XOR property:
A ^ A = 0

This implies:
If Ciphertext = 00, then Plaintext == Key at that position.
If Plaintext = 00, then Ciphertext == Key.
These observations strongly suggest a repeating-key XOR cipher.

2. Hypothesis & Testing
I pursued two parallel attack vectors.

Attack Vector 1: Repeated Pattern 16041045 (Known-Plaintext Attack)
The text is clearly English. The most common word that begins a sentence in English is "The " (four characters: T, h, e, and a space).
I performed crib dragging as follows:

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

This yields the first key fragment: Blue

This result is highly plausible (e.g., “Blue Team”).
I then tested the next four bytes of the first line (16091408), assuming the following word was "Team".

0x16 ^ 'B' = 'T' (valid)

0x09 ^ 'l' = 'e' (valid)

…

This confirmed the full key: BlueTeam

Attack Vector 2: Lines with 00000000
I examined the second line:
00000000 7431...

If the cipher byte is 00, then:
Plaintext byte == Key byte

Therefore, the first four characters of this line are identical to the first four characters of the key.
Even without knowing the key beforehand, the bytes following the zeros (74 31 04 0c ...) can be tested.
Using the key BlueTeam inferred from Attack Vector 1:
0x74 ^ 'T' (5th character of the key) produces meaningful output.
Combining both attack vectors, I concluded with 99.9% confidence that the key is:
BlueTeam

3. Writing the Decryption Script (Exploitation)
Once the key was identified, I automated the process using a small Python script rather than continuing manual calculations.
Script logic:
Iterate through each line of hexadecimal input.
->Convert hex strings into byte arrays.
->XOR each byte with the corresponding character of the repeating key BlueTeam (using modulo indexing).
->Print the decoded plaintext.
(The script is identical to the one provided in the previous response.)

4. Post-Exploitation Analysis
After running the script, the recovered plaintext was easily readable.
The content discusses security concepts, specifically the definitions and roles of Blue Team and Red Team in cybersecurity.

5. Summary
Encryption type: Vigenère cipher (more precisely, Repeating-Key XOR)
Key weaknesses:
Short, repeating key
Information leakage via 00 bytes (plaintext equals key)
Predictable, common plaintext at sentence beginnings (“The ”)
Recovered key: BlueTeam

## Directory Structure

```
.
│  ciphertexts2.txt
│  main.py
│  readme.md
│  test1_1.py
│  test1_2.py
│  test2_1.py
│  test2_2.py
│  test2_3.py
│  test2_4.py
│  test2_5.py
└── __pycache__/
```

---

## File Descriptions and Analysis Flow

### `ciphertexts2.txt`

Contains the raw ciphertext lines in hexadecimal form. Each line represents one message encrypted using the same repeating XOR key.

---

### Phase 1: Reconnaissance and Pattern Discovery

#### `test1_1.py`

Purpose:

* Loads the ciphertext file.
* Splits the content into individual lines.
* Prints basic statistics such as the total number of lines and a preview of the first few entries.

This script is used to gain an initial overview of the dataset.

---

#### `test1_2.py`

Purpose:

* Analyzes the ciphertext lines to detect repeated prefixes.
* Counts how many lines start with the same first 4 bytes (8 hex characters).
* Identifies lines that start with `00000000`.

Findings:

* Many lines share the prefix `16041045`, suggesting a repeated plaintext prefix.
* Several lines begin with null bytes, a known weakness in XOR encryption.

---

### Phase 2: Known-Plaintext and Key Recovery

#### `test2_1.py`

Purpose:

* Tests the hypothesis that the repeated prefix `16041045` corresponds to the plaintext `"The "`.
* Performs XOR between the guessed plaintext and ciphertext to recover the first key fragment.

Result:

* Successfully recovers the key fragment: `Blue`.

---

#### `test2_2.py`

Purpose:

* Extends the key by testing plausible continuations after `Blue`.
* Tries common words such as `Team`, `Flag`, etc.
* Checks whether the XOR results maintain a consistent repeating-key pattern.

Result:

* `Team` correctly continues the key, forming `BlueTeam`.

---

#### `test2_3.py`

Purpose:

* Verifies the full candidate key `BlueTeam`.
* Uses it to decrypt the first ciphertext line.

Result:

* The decrypted output is readable English, strongly confirming the correctness of the key.

---

### Phase 3: Exploiting Null Bytes

#### `test2_4.py`

Purpose:

* Analyzes a line that starts with `00000000`.
* Counts how many leading null bytes appear.
* Explains the implication: when the ciphertext byte is `0x00`, the plaintext byte equals the key byte.

This script provides additional theoretical confirmation of the recovered key.

---

#### `test2_5.py`

Purpose:

* Uses the recovered key `BlueTeam` to decrypt a line containing null bytes.
* Displays both the decrypted text and a byte-by-byte XOR breakdown.

Result:

* The output is meaningful English text, further validating the attack.

---

### Phase 4: Full Decryption

#### `main.py`

Purpose:

* Contains the full ciphertext dataset inline.
* Implements a reusable XOR decryption function.
* Iterates through all ciphertext lines and prints the fully decrypted plaintext.

Result:

* Successfully recovers the complete plaintext, which discusses cybersecurity concepts such as Blue Team and Red Team roles.

---

## Conclusion

* Cipher type: Repeating-key XOR (Vigenère-style)
* Recovered key: `BlueTeam`
* Main weaknesses exploited:

  * Short, repeating key
  * Repeated plaintext prefixes
  * Presence of null bytes (`0x00`) in ciphertext
  * Predictable English sentence openings

This project illustrates how basic statistical analysis and known-plaintext attacks can fully break improperly used XOR encryption.
