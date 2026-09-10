# users/user_manager.py
import os
from crypto.ecc_cipher import ECCCipher
from config import USERS

class UserManager:
    def __init__(self):
        self.ecc = ECCCipher()
        self.user_keys = {}
        self.user_info = {}

    def setup_all_users(self):
        os.makedirs("users/keys", exist_ok=True)
        keypairs = {}
        for user_id in USERS.keys():
            priv, pub = self.ecc.generate_keypair()
            keypairs[user_id] = (priv, pub)
            self.ecc.save_keys(priv, pub, user_id)
            self.user_info[user_id] = dict(USERS[user_id])

        owner_priv, owner_pub = keypairs["owner"]
        for user_id, (user_priv, user_pub) in keypairs.items():
            if user_id == "owner":
                continue
            owner_shared = self.ecc.derive_shared_key(owner_priv, user_pub)
            user_shared = self.ecc.derive_shared_key(user_priv, owner_pub)
            assert owner_shared == user_shared
            self.user_keys[user_id] = owner_shared

        self.user_keys["owner"] = self.ecc.derive_shared_key(owner_priv, keypairs["user1"][1])

        print(f"[OK] {len(USERS)} users setup complete: {list(USERS.keys())}")
        return self.user_keys

    def get_key(self, user_id: str):
        return self.user_keys.get(user_id)

    def can_upload(self, user_id: str) -> bool:
        return self.user_info.get(user_id, {}).get("can_upload", False)

    def can_search(self, user_id: str) -> bool:
        return self.user_info.get(user_id, {}).get("can_search", False)

    def get_role(self, user_id: str) -> str:
        return self.user_info.get(user_id, {}).get("role", "unknown")

    def is_keyword_allowed(self, user_id: str, keyword: str) -> bool:
        """Check if user is allowed to search this keyword"""
        allowed = self.user_info.get(user_id, {}).get("allowed_keywords", "*")
        if allowed == "*":
            return True
        return keyword.lower() in [k.lower() for k in allowed]

    def grant_upload(self, user_id: str):
        if user_id in self.user_info:
            self.user_info[user_id]["can_upload"] = True
            print(f"[OK] Upload access granted to '{user_id}'")

    def revoke_upload(self, user_id: str):
        if user_id in self.user_info:
            self.user_info[user_id]["can_upload"] = False
            print(f"[OK] Upload access revoked from '{user_id}'")