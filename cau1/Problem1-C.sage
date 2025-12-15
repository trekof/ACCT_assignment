# ==========================================
# STEP 1: PREPARE THE DATA
# ==========================================
print("--- STEP 1: DATA GENERATION ---")

# 1. Pick a random hidden integer X
hidden_X = ZZ.random_element(1000, 100000)
print(f"Hidden Integer X: {hidden_X}")

# 2. compute the square root
# We need high precision to make the "approximate zero"
RR_prec = RealField(200) 
beta = RR_prec(sqrt(hidden_X))
print(f"Computed sqrt(X) (beta): {beta}")

# 3. Define the degree and scaling constant
# We are looking for a degree 2
n = 2 
d = 40 # Precision depth
C = 10**d 
print(f"Scaling Constant C (10^{d}): 10^{d}")
print("\n")


# ==========================================
# STEP 2: BUILD THE LATTICE BASIS
# ==========================================
print("--- STEP 2: BUILDING THE LATTICE ---")
print("We construct a matrix where rows represent powers of beta.")
print("Row format: [coeff_c0, coeff_c1, coeff_c2,  Weighted_Value]")

matrix_rows = []

# Row for c0 (Constant term 1)
# Vector: [1, 0, 0, floor(C * 1)]
r0 = [1, 0, 0, floor(C * 1)]
matrix_rows.append(r0)
print(f"Row 0 (represents 1):   {r0}")

# Row for c1 (Linear term beta)
# Vector: [0, 1, 0, floor(C * beta)]
r1 = [0, 1, 0, floor(C * beta)]
matrix_rows.append(r1)
print(f"Row 1 (represents beta): {r1}")

# Row for c2 (Quadratic term beta^2)
# Vector: [0, 0, 1, floor(C * beta^2)]
r2 = [0, 0, 1, floor(C * beta**2)]
matrix_rows.append(r2)
print(f"Row 2 (represents beta^2): {r2}")

# Create the Matrix
L = Matrix(ZZ, matrix_rows)
print("\n")


# ==========================================
# STEP 3: LATTICE REDUCTION (LLL)
# ==========================================
print("--- STEP 3: RUNNING LLL ALGORITHM ---")
print("The LLL algorithm will now look for short linear combinations of the rows above.")
print("It is trying to minimize the last column (the weighted value).")

L_reduced = L.LLL()

print("Reduction complete. Here are the new rows found by LLL:")
for i, row in enumerate(L_reduced.rows()):
    print(f"New Row {i}: {row}")

print("\n")


# ==========================================
# STEP 4: INTERPRETING THE RESULT
# ==========================================
print("--- STEP 4: DECODING THE ANSWER ---")

# Usually the first row (or the one with the smallest norms) is our answer.
candidate_vector = L_reduced[0]
print(f"Shortest Vector Selected: {candidate_vector}")

# Extract coefficients (first 3 numbers)
c0 = candidate_vector[0]
c1 = candidate_vector[1]
c2 = candidate_vector[2]
error_term = candidate_vector[3]

print(f"\nPolynomial Coefficients found:")
print(f"c0 (Constant): {c0}")
print(f"c1 (Linear):   {c1}")
print(f"c2 (Square):   {c2}")

# Construct the Polynomial
R.<t> = PolynomialRing(ZZ)
poly = c2*t^2 + c1*t + c0

print(f"\nReconstructed Polynomial: {poly}")

# Check if it matches t^2 - X
if abs(c0) == hidden_X and c2 == 1:
    print(f"SUCCESS! We found the polynomial t^2 - {abs(c0)}")
    print(f"The hidden integer X was: {abs(c0)}")
elif abs(c0) == hidden_X and c2 == -1:
    # Sometimes LLL gives the vector with flipped signs (-t^2 + X)
    print(f"SUCCESS! We found the polynomial -t^2 + {abs(c0)}")
    print(f"The hidden integer X was: {abs(c0)}")
else:
    print("Failed to reconstruct exactly. Check precision (d) or C.")