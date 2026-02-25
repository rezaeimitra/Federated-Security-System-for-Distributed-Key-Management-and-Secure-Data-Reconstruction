from cryptography.fernet import Fernet

# کلید recover شده prototype
key = b"d155464b54aeec12247057d4f86ba427"
fernet_key = Fernet.generate_key()  # کلید امن symmetric برای تست
cipher = Fernet(fernet_key)

secret_data = b"This is EDGE Secure Partition Data!"
encrypted = cipher.encrypt(secret_data)

with open("secure_partition.bin", "wb") as f:
    f.write(encrypted)

print("Encrypted Partition created as secure_partition.bin")
print("Decryption key for test (fernet):", fernet_key.decode())
