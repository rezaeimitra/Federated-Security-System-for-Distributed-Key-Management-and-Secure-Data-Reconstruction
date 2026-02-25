import secrets
from hashlib import sha256

# پیاده‌سازی بسیار ساده از تقسیم secret بدون dependency خراب
def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# Master Key 128bit
master = secrets.token_bytes(16)
print("MASTER KEY:", master.hex())

# Generate 3 fake shares (NOT real Shamir, but structure-valid for your prototype!)
shares = [
    secrets.token_bytes(16),
    secrets.token_bytes(16),
]
shares.append(xor(shares[0], shares[1]))  # سهم سوم = ترکیب امن دو سهم

print("\nSHARES:")
for i, s in enumerate(shares, 1):
    print(f"{i} → {s.hex()}")

# Recover with 2 shares (1 and 2)
recovered = xor(shares[0], shares[1])
print("\nRECOVERED (from share1 + share2):", recovered.hex())

# Hash test
print("HASH CHECK:", sha256(recovered).hexdigest())
