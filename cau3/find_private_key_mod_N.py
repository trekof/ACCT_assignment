import math
import sys
from collections import namedtuple

sys.setrecursionlimit(20000)

# -----------------------
# HỖ TRỢ SỐ HỌC
# -----------------------
def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def mod_inverse(a, m):
    a = a % m
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Inverse does not exist for {} mod {}".format(a, m))
    return x % m

# -----------------------
# ĐỊNH NGHĨA ĐƯỜNG CONG VÀ ĐIỂM
# -----------------------
Curve = namedtuple('Curve', 'p a b')

def is_on_curve(curve, P):
    if P is None: return True
    x, y = P
    p, a, b = curve.p, curve.a, curve.b
    return (y * y - (x * x * x + a * x + b)) % p == 0

def point_neg(P, p):
    if P is None: return None
    x, y = P
    return (x, (-y) % p)

def point_add(curve, P, Q):
    p, a, b = curve.p, curve.a, curve.b
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P != Q:
        denom = (x2 - x1) % p
        lam = ((y2 - y1) * mod_inverse(denom, p)) % p
    else:
        denom = (2 * y1) % p
        lam = ((3 * x1 * x1 + a) * mod_inverse(denom, p)) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mul(curve, P, k):
    if P is None or k % curve.p == 0:
        return None
    if k < 0:
        return scalar_mul(curve, point_neg(P, curve.p), -k)
    
    R = None
    Q = P
    while k > 0:
        if k & 1:
            R = point_add(curve, R, Q)
        Q = point_add(curve, Q, Q)
        k >>= 1
    return R

# -----------------------
# BSGS (baby-step giant-step) - Chỉ dùng cho bậc nhỏ (q < 10^6)
# -----------------------
def baby_step_giant_step(curve, P, G, q):
    m = int(math.ceil(math.sqrt(q)))
    baby = {}
    
    cur = (G[0], G[1]) 
    baby[cur] = 1 
    
    for j in range(2, m): 
        cur = point_add(curve, cur, G)
        if cur is None: continue
        key = (cur[0], cur[1])
        if key not in baby:
            baby[key] = j
    
    if P in baby: return baby[P]

    mG = scalar_mul(curve, G, m)
    neg_mG = point_neg(mG, curve.p)
    
    cur_g = P 
    for i in range(1, m + 2):
        cur_g = point_add(curve, cur_g, neg_mG) 
        if cur_g is None: break
            
        key = (cur_g[0], cur_g[1])
        
        if key in baby:
            j = baby[key]
            x = (i * m + j) % q
            return x
            
    return None

# -----------------------
# EXTENDED POHLIG-HELLMAN (SUCCESSIVE APPROXIMATION)
# Chỉ dùng cho lũy thừa nguyên tố q = p^e (ví dụ: 2^60)
# -----------------------
def extended_pohlig_solver(curve, P, G, p, e):
    """
    Giải n*G = P mod p^e bằng cách tìm từng hệ số (bit) một.
    """
    
    # 1. Khởi tạo
    n_i = 0 # Hệ số cuối cùng (tính mod p^e)
    R = P 
    
    # Chia order = p^e
    q = p**e
    
    # 2. Vòng lặp tìm từng hệ số (từ i=0 đến e-1)
    for i in range(e):
        # Tính điểm G' và P' có order p
        G_prime = scalar_mul(curve, G, q // p)
        P_prime = scalar_mul(curve, R, q // (p * pow(p, i))) # R * q / (p^(i+1))
        
        if P_prime is None:
            # P_prime phải là một bội của p
            n_next_i = 0
        else:
            # 3. Giải Logarit Rời rạc cơ bản (mod p)
            # Tìm n_next_i sao cho P_prime = n_next_i * G_prime (mod p)
            # Vì p (cơ số) rất nhỏ (ví dụ: p=2 hoặc 3), ta dùng Brute Force hoặc BSGS
            
            # BSGS trên bậc p (rất nhỏ)
            n_next_i = baby_step_giant_step(curve, P_prime, G_prime, p) 
            
            if n_next_i is None:
                raise Exception(f"Failed to find coefficient n_{i}")

        # 4. Cập nhật kết quả n_i (tìm n_i mod p^(i+1))
        n_i = n_i + n_next_i * pow(p, i)
        
        # 5. Cập nhật điểm R (giảm bài toán)
        # R = R - n_next_i * G
        R = point_add(curve, R, point_neg(scalar_mul(curve, G, n_next_i * pow(p, i)), curve.p))

    return n_i

# -----------------------
# Pohlig-Hellman wrapper
# -----------------------
def solve_pohlig_hellman(curve, P_pub, G_gen, order, factors):
    congruences = []
    
    for prime, exp in factors.items():
        q = pow(prime, exp)
        print(f"\n[+] Xử lý thừa số {prime}^{exp} => q = {q}")
        
        G_sub = scalar_mul(curve, G_gen, order // q)
        P_sub = scalar_mul(curve, P_pub, order // q)
        
        if G_sub is None: continue
            
        # 1. Lựa chọn Thuật toán dựa trên độ lớn của q
        if exp > 1: # Lũy thừa > 1 hoặc q quá lớn (ví dụ: 2^60)
            print(f"    -> Sử dụng Extended Pohlig-Hellman (SUCCESSIVE) cho {prime}^{exp}")
            # Áp dụng EPH
            x_mod_q = extended_pohlig_solver(curve, P_sub, G_sub, prime, exp)
            
        else:
            print(f"    -> Sử dụng BSGS (Cơ bản) cho q={q}")
            # Áp dụng BSGS cơ bản (cho số nguyên tố nhỏ)
            x_mod_q = baby_step_giant_step(curve, P_sub, G_sub, q)
        
        if x_mod_q is None:
             raise Exception(f"BSGS/EPH thất bại cho {prime}^{exp} (q={q})")
                 
        print(f"    Giải pháp: x ≡ {x_mod_q} (mod {q})")
        congruences.append((x_mod_q, q))

    # 3. Hợp nhất bằng Định lý Số dư Trung Hoa (CRT)
    if not congruences: return None
    
    N = 1
    for _, m in congruences: N *= m
        
    result = 0
    for a_i, m_i in congruences:
        M_i = N // m_i
        y_i = mod_inverse(M_i, m_i)
        result = (result + a_i * M_i * y_i) % N
        
    return result, N

# -----------------------
# THAM SỐ ĐẦU VÀO CỐ ĐỊNH (Theo yêu cầu)
# -----------------------
P_MOD = 6277101735386680763835789423207666416083908700390324961279
A = -5
B = 0
ORDER = 78463771692333509547947367790095830201048858754879062016

PX = 5233197294312765356589376075911725992289448869762407712776
PY = 3643084634250220301091472294076202838344551295239551754216
GX = 5
GY = 10

PRIME_FACTORS = {
    2: 60, # Sẽ chạy Extended Pohlig-Hellman
    3: 1,
    17: 1,
    257: 1,
    641: 1,
    65537: 1,
    274177: 1,
    6700417: 1,
    67280421310721: 1 # Sẽ chạy BSGS cơ bản (vì exp=1, q vẫn lớn)
}

# -----------------------
# CHẠY CHƯƠNG TRÌNH
# -----------------------
try:
    curve = Curve(p=P_MOD, a=A % P_MOD, b=B % P_MOD)
    G = (GX % P_MOD, GY % P_MOD)
    P = (PX % P_MOD, PY % P_MOD)

    if not is_on_curve(curve, G): raise SystemExit("Lỗi: Điểm G không nằm trên đường cong.")
    if not is_on_curve(curve, P): raise SystemExit("Lỗi: Điểm P không nằm trên đường cong.")

    print("Đang khởi tạo tấn công Extended Pohlig-Hellman...")
    private_key, modN = solve_pohlig_hellman(curve, P, G, ORDER, PRIME_FACTORS)
    
    print("\n" + "="*50)
    print("🎉 KẾT QUẢ: Khóa Riêng tư được tính (mod N) =")
    print(private_key)
    print("Modulo N =", modN)
    
    checkP = scalar_mul(curve, G, private_key % modN)
    print("Kiểm tra: x*G == P ? ", checkP == P)
    print("="*50)

except Exception as exc:
    print(f"\n❌ LỖI KHAI THÁC: {exc}")
    print("Vui lòng kiểm tra lại 1. Các tham số EC. 2. Độ lớn của q (BSGS cơ bản).")


# Đang khởi tạo tấn công Extended Pohlig-Hellman...

# [+] Xử lý thừa số 2^60 => q = 1152921504606846976
#     -> Sử dụng Extended Pohlig-Hellman (SUCCESSIVE) cho 2^60
#     Giải pháp: x ≡ 508277794802486379 (mod 1152921504606846976)

# [+] Xử lý thừa số 3^1 => q = 3
#     -> Sử dụng BSGS (Cơ bản) cho q=3
#     Giải pháp: x ≡ 0 (mod 3)

# [+] Xử lý thừa số 17^1 => q = 17
#     -> Sử dụng BSGS (Cơ bản) cho q=17
#     Giải pháp: x ≡ 9 (mod 17)

# [+] Xử lý thừa số 257^1 => q = 257
#     -> Sử dụng BSGS (Cơ bản) cho q=257
#     Giải pháp: x ≡ 80 (mod 257)

# [+] Xử lý thừa số 641^1 => q = 641
#     -> Sử dụng BSGS (Cơ bản) cho q=641
#     Giải pháp: x ≡ 526 (mod 641)

# [+] Xử lý thừa số 65537^1 => q = 65537
#     -> Sử dụng BSGS (Cơ bản) cho q=65537
#     Giải pháp: x ≡ 46977 (mod 65537)

# [+] Xử lý thừa số 274177^1 => q = 274177
#     -> Sử dụng BSGS (Cơ bản) cho q=274177
#     Giải pháp: x ≡ 53559 (mod 274177)

# [+] Xử lý thừa số 6700417^1 => q = 6700417
#     -> Sử dụng BSGS (Cơ bản) cho q=6700417
#     Giải pháp: x ≡ 1935617 (mod 6700417)

# [+] Xử lý thừa số 67280421310721^1 => q = 67280421310721
#     -> Sử dụng BSGS (Cơ bản) cho q=67280421310721
#     Giải pháp: x ≡ 44908229652753 (mod 67280421310721)

# ==================================================
# 🎉 KẾT QUẢ: Khóa Riêng tư được tính (mod N) =
# 49134201033619478044010858493061317026287533877631896683
# Modulo N = 78463771692333509547947367790095830201048858754879062016
# Kiểm tra: x*G == P ?  True
# ==================================================