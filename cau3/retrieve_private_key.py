
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
# THAM SỐ ĐẦU VÀO CỐ ĐỊNH (Theo yêu cầu)
# -----------------------
P_MOD = 6277101735386680763835789423207666416083908700390324961279
A = -3
B = 2455155546008943817740293915197451784769108058161191238065
ORDER = 6277101735386680763835789423176059013767194773182842284081

GX = 3289624317623424368845348028842487418520868978772050262753
GY = 5673242899673324591834582889556471730778853907191064256384
PX = 2666414626355054857763276393201319872259043665306389055696
PY = 1654459546843298559173321782246873016120528804748946449578

# -----------------------
# CHẠY CHƯƠNG TRÌNH
# -----------------------
try:
    curve = Curve(p=P_MOD, a=A % P_MOD, b=B % P_MOD)
    G = (GX % P_MOD, GY % P_MOD)
    P = (PX % P_MOD, PY % P_MOD)

    if not is_on_curve(curve, G): raise SystemExit("Lỗi: Điểm G không nằm trên đường cong.")
    if not is_on_curve(curve, P): raise SystemExit("Lỗi: Điểm P không nằm trên đường cong.")

    print("Đang dò tìm key...")

    for i in range(-100,100):
        private_key = 49134201033619478044010858493061317026287533877631896683+i*78463771692333509547947367790095830201048858754879062016
        checkP = scalar_mul(curve, G, private_key%ORDER)
        print("Kiểm tra: x*G == P ? ", checkP == P)
        if checkP == P:
            print("Tìm thấy khóa bí mật chính xác!")
            print("gia trị i =", i)
            print("Khóa bí mật x =", private_key%ORDER)
        print("="*50)

except Exception as exc:
    print(f"\n❌ LỖI KHAI THÁC: {exc}")


# ==================================================
# Kiểm tra: x*G == P ?  True
# Tìm thấy khóa bí mật chính xác!
# gia trị i = 23
# Khóa bí mật x = 1853800949957290197646800317665265411650411285239850323051