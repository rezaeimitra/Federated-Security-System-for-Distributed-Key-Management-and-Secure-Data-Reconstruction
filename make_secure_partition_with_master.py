# make_secure_partition_with_master.py
import binascii
from hashlib import sha256
import base64
from cryptography.fernet import Fernet
from pathlib import Path

# master_key.txt که توسط key_generator_for_containers.py ساخته شده را بخوان
master_hex = Path("master_key.txt").read_text().strip()
master = binascii.unhexlify(master_hex)

# derive fernet key
fernet_key = base64.urlsafe_b64encode(sha256(master).digest())
f = Fernet(fernet_key)

secret_data = b"This is EDGE Secure Partition Data! (protected by federation)\n"
encrypted = f.encrypt(secret_data)

Path("secure").mkdir(exist_ok=True)
with open("secure/secure_partition.bin", "wb") as fh:
    fh.write(encrypted)

print("Wrote secure/secure_partition.bin using master from master_key.txt")
print("fernet key (base64):", fernet_key.decode())
