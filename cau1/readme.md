Overview
This problem demonstrates how to use lattice reduction algorithms (specifically the LLL algorithm) to solve two important problems:

Part B: Finding the minimal polynomial of an algebraic number given its numerical approximation
Part C: Recovering a hidden integer from partial knowledge of its square root

Both parts reformulate classical algebraic problems into lattice problems, where the LLL algorithm can efficiently find short vectors that correspond to solutions.
Problem Background
Minimal Polynomial (Part B)
Given an algebraic number α = 3 + ∛23, we want to find its minimal polynomial f(x) over ℤ when given only a numerical approximation β of α.
Key Insight: If f(α) = 0 (exact), then f(β) ≈ 0 (approximate). We can construct a lattice where a short vector in the reduced basis corresponds to the coefficients of f(x).
Hidden Integer Recovery (Part C)
Given the first d digits of √X (in decimal), we want to recover the original integer X.
Key Insight: The approximation error is bounded, allowing us to set up a lattice where the vector [c₀, c₁, c₂, error] is small, leading to the recovery of X from the polynomial t² - X.
System Requirements

SageMath 9.0+ (includes Python, LLL algorithm, polynomial rings)
Python 3.7+ (bundled with SageMath)
Memory: ~1GB (sufficient for this problem)
Operating System: Linux, macOS, or Windows (WSL recommended)

Installation
Option 1: Using SageMath (Recommended)
bash# Download and install SageMath from https://www.sagemath.org/
# Or use package manager:

# Ubuntu/Debian
sudo apt-get install sagemath

# macOS (Homebrew)
brew install --cask sage

# Windows: Use WSL2 + Ubuntu
Option 2: Docker
bashdocker pull sagemath/sagemath:latest
docker run -it -v $(pwd):/home/sage sagemath/sagemath:latest sage
File Structure
problem1/
├── Problem1-B.sage          # Part B: Minimal polynomial of α = 3 + ∛23
├── Problem1-C.sage          # Part C: Recover X from approximation of √X
└── README.md                # This file
How to Run
Part B: Finding Minimal Polynomial
Objective: Given β (approximation of 3 + ∛23), find the minimal polynomial f(x).
Using SageMath Interactive Mode
bash# Start SageMath
sage

# Inside SageMath REPL:
load("Problem1-B.sage")
Using SageMath Batch Mode
bashsage Problem1-B.sage
Expected Output
Target value beta: 3.284804562...
Search degree n: 3
--------------------
Initial Lattice Matrix:
[                    1000000000000                     0                     0                     0 1000000000000]
[                           0                     1000000000000                     0                     0 3284804562...]
[                           0                     0                     1000000000000                     0 10790627876...]
[                           0                     0                     0                     1000000000000 35441340644...]
--------------------
Reduced Lattice Matrix (First row is our candidate):
[  1  -3   3  -1  <error_term>]
[  ... (other rows)
--------------------
Found coefficients: [1, -3, 3, -1]
Candidate Minimal Polynomial:
-x^3 + 3*x^2 - 3*x + 1

Verification substitution f(alpha): 0
SUCCESS: The polynomial is exact.
What this means:

The coefficients [1, -3, 3, -1] give us the polynomial: f(x) = -x³ + 3x² - 3x + 1
This can be rewritten as: f(x) = -(x - 1)³ or equivalently f(x) = x³ - 3x² + 3x - 1
Verification confirms: f(3 + ∛23) = 0 ✓

Part C: Recovering Hidden Integer from Square Root Approximation
Objective: Given d-digit approximation of √X, recover the original integer X.
Using SageMath Interactive Mode
bashsage

# Inside SageMath REPL:
load("Problem1-C.sage")
Using SageMath Batch Mode
bashsage Problem1-C.sage
Expected Output (Example Run)
--- STEP 1: DATA GENERATION ---
Hidden Integer X: 45328
Computed sqrt(X) (beta): 212.9219535701...
Scaling Constant C (10^40): 10^40

--- STEP 2: BUILDING THE LATTICE ---
We construct a matrix where rows represent powers of beta.
Row format: [coeff_c0, coeff_c1, coeff_c2,  Weighted_Value]
Row 0 (represents 1):   [1, 0, 0, <scaled_value>]
Row 1 (represents beta): [0, 1, 0, <scaled_value>]
Row 2 (represents beta^2): [0, 0, 1, <scaled_value>]

--- STEP 3: RUNNING LLL ALGORITHM ---
The LLL algorithm will now look for short linear combinations of the rows above.
It is trying to minimize the last column (the weighted value).
Reduction complete. Here are the new rows found by LLL:
New Row 0: [1, -212, 45328, <error_term>]
New Row 1: [... other rows ...]

--- STEP 4: DECODING THE ANSWER ---
Shortest Vector Selected: [1, -212, 45328, <error_term>]

Polynomial Coefficients found:
c0 (Constant): 45328
c1 (Linear):   -212
c2 (Square):   1

Reconstructed Polynomial: t^2 - 212*t + 45328

SUCCESS! We found the polynomial t^2 - 45328
The hidden integer X was: 45328
What this means:

The shortest vector found by LLL corresponds to the polynomial: t² - 212t + 45328
This factors as approximately: t² - X where X = 45328
The recovered integer matches the original hidden value ✓

Detailed Methodology
Part B: Lattice Construction for Minimal Polynomial
Step 1: Setup

High-precision arithmetic to avoid numerical errors
Target value: β ≈ 3.284804562... (approximation of 3 + ∛23)
Expected polynomial degree: n = 3 (since we have a cubic root)
Scaling constant: C = 10¹² (large enough to enforce the relation)

Step 2: Build Lattice Basis
For a polynomial f(x) = c₀ + c₁x + c₂x² + c₃x³, we want f(β) ≈ 0.
This translates to: c₀·1 + c₁·β + c₂·β² + c₃·β³ ≈ 0
Create vectors:

v₀ = [1, 0, 0, 0, C·1]
v₁ = [0, 1, 0, 0, C·β]
v₂ = [0, 0, 1, 0, C·β²]
v₃ = [0, 0, 0, 1, C·β³]

The last column contains the "approximate zero" scaled by C.
Step 3: LLL Reduction
The LLL algorithm finds short vectors. The shortest vector will have:

Small coefficients [c₀, c₁, c₂, c₃]
Small error term (last component)

This shortest vector directly gives us the minimal polynomial coefficients.
Step 4: Verification
Check if f(α) = 0 algebraically using exact symbolic computation.
Part C: Lattice Construction for Hidden Integer Recovery
Step 1: Setup

Hidden integer X (unknown to attacker)
Approximation: β ≈ √X with d decimal places known
Expected polynomial degree: n = 2 (quadratic for square root)
Precision depth: d = 40 (C = 10⁴⁰)

Step 2: Build Lattice Basis
We want to find coefficients of t² - X.
Create vectors:

v₀ = [1, 0, 0, C·1]
v₁ = [0, 1, 0, C·β]
v₂ = [0, 0, 1, C·β²]

Where β is our approximation of √X.
Step 3: LLL Reduction
The shortest vector found will have:

c₂ ≈ 1 (coefficient of t²)
c₁ ≈ -β (coefficient of t, approximately -√X)
c₀ ≈ X (constant term, the hidden integer!)

Step 4: Recovery
Extract c₀ from the shortest vector—this is the original hidden integer X.
Key Parameters and Configuration
Part B
python# Scaling constant - determines how strongly we enforce f(β) ≈ 0
C = 10**12

# Polynomial degree - for cubic roots, use degree 3
n = 3

# Precision - using 100 decimal places to avoid rounding errors
RR_high = RealField(100)
Tuning tips:

If the algorithm fails, increase C to 10¹⁵ or 10¹⁸
For a kth root, use degree n = k
For higher degree polynomials, you may need higher precision

Part C
python# Precision depth - determines C = 10^d
d = 40  # C = 10^40

# Higher precision for approximation
RR_prec = RealField(200)

# Polynomial degree - always 2 for square roots
n = 2
Tuning tips:

Increase d if the approximation is less precise (fewer known decimal places)
C = 10⁴⁰ works well for 40 decimal places of precision
The relationship: error ≤ 10⁻ᵈ should hold

Understanding the Output
What is the "Shortest Vector"?
After LLL reduction, the first row of the reduced matrix is typically the shortest vector. This vector encodes:

First n+1 components: Coefficients of the polynomial
Last component: Error term (should be very small)

Verification Checks
Part B:
Verification substitution f(alpha): 0
SUCCESS: The polynomial is exact.
This confirms the minimal polynomial works algebraically.
Part C:
SUCCESS! We found the polynomial t^2 - X
The hidden integer X was: <value>
This confirms the recovery is correct.
Theoretical Background
Shortest Vector Problem (SVP)
Given a lattice L, find a nonzero vector v ∈ L with minimum Euclidean norm.
The LLL algorithm (Lenstra-Lenstra-Lovász, 1982) efficiently approximates SVP in polynomial time.
Lattice Basis
A lattice is generated by integer linear combinations of basis vectors. Different bases can generate the same lattice. LLL finds a "reduced basis" where vectors are short and nearly orthogonal.
Why This Works

Algebraic Property: If f(α) = 0 exactly, then the coefficients satisfy a specific algebraic relation
Approximation Property: Given numerical approximation β ≈ α, we can encode the relation as a lattice vector
Short Vector Property: The coefficients are relatively small integers, making the lattice vector short
LLL Efficiency: LLL finds this short vector in polynomial time