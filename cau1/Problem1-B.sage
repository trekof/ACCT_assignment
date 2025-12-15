# 1. Setup the parameters
# We want to find the minimal polynomial for alpha = 3 + 23^(1/3)
# We will simulate the "approximation" step by computing it numerically first.

# Create a high-precision field to ensure our internal calculations are accurate
RR_high = RealField(100) 

# Define the target value alpha
alpha_exact = 3 + 23**(1/3)
beta = RR_high(alpha_exact)

# Degree of the polynomial we are looking for (n=3 for cube roots)
n = 3 

# The scaling constant C.
# It determines the weight of the "approximate zero" equation.
# It should be large enough to enforce the relation.
C = 10**12 

print(f"Target value beta: {beta}")
print(f"Search degree n: {n}")
print("-" * 20)

# 2. Construct the Lattice Basis Matrix
# We build a matrix with n+1 rows and n+2 columns.
# The rows represent the basis vectors: v_i = (0...1...0, floor(C * beta^i))
matrix_rows = []

for i in range(n + 1):
    vec = [0] * (n + 1)
    vec[i] = 1
    
    # Append the scaled approximation part: floor(C * beta^i)
    val = floor(C * (beta**i))
    vec.append(val)
    
    matrix_rows.append(vec)

# Create the matrix in Sage
L = Matrix(ZZ, matrix_rows)

print("Initial Lattice Matrix:")
print(L)
print("-" * 20)

# 3. Apply LLL Reduction
# LLL will find a basis of short vectors. The first row is usually the shortest.
L_reduced = L.LLL()

print("Reduced Lattice Matrix (First row is our candidate):")
print(L_reduced)
print("-" * 20)

# 4. Extract the Polynomial
# The first row of the reduced matrix contains coefficients [c0, c1, c2, c3, error_term]
shortest_vector = L_reduced[0]

# Define the polynomial ring
R.<x> = PolynomialRing(ZZ)

# Construct the polynomial using the first n+1 components of the vector
# Note: The vector is [c0, c1, c2, c3, ...], which maps to c0 + c1*x + c2*x^2 + c3*x^3
coeffs = shortest_vector[:n+1]
f = sum(coeffs[i] * x**i for i in range(len(coeffs)))

print("Found coefficients:", coeffs)
print("Candidate Minimal Polynomial:")
show(f) # Pretty print the polynomial

# 5. Verification
# Check if f(alpha) is actually zero (algebraically)
check = f.subs(x=alpha_exact)

print(f"\nVerification substitution f(alpha): {check.expand()}")
if check.expand() == 0:
    print("SUCCESS: The polynomial is exact.")
else:
    print("FAILURE: The polynomial is not exact (approximation error or degree too low).")