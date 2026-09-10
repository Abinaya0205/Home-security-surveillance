from .ecc_cipher import ECCCipher
from .aes_cipher import AESCipher
import os

class HybridCrypto:
    def __init__(self):
        self.ecc = ECCCipher()
        self.aes = AESCipher()

    def setup_users(self, owner_id="owner", user_id="user1"):
        owner_priv, owner_pub = self.ecc.generate_keypair()
        user_priv, user_pub = self.ecc.generate_keypair()
        self.ecc.save_keys(owner_priv, owner_pub, owner_id)
        self.ecc.save_keys(user_priv, user_pub, user_id)
        owner_shared = self.ecc.derive_shared_key(owner_priv, user_pub)
        user_shared = self.ecc.derive_shared_key(user_priv, owner_pub)
        assert owner_shared == user_shared
        print(f"[OK] Users '{owner_id}' and '{user_id}' setup complete.")
        return owner_shared

    def encrypt_file(self, filepath: str, key: bytes) -> str:
        with open(filepath, "rb") as f:
            data = f.read()
        encrypted = self.aes.encrypt(data, key)
        os.makedirs("cloud", exist_ok=True)
        out_path = "cloud/" + os.path.basename(filepath) + ".enc"
        with open(out_path, "wb") as f:
            f.write(encrypted)
        return out_path

    def decrypt_file(self, enc_path: str, key: bytes, out_path: str):
        with open(enc_path, "rb") as f:
            encrypted = f.read()
        decrypted = self.aes.decrypt(encrypted, key)
        with open(out_path, "wb") as f:
            f.write(decrypted)
        return out_path