from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
import os

class AESCipher:
    @staticmethod
    def encrypt(plaintext: bytes, key: bytes) -> bytes:
        iv = os.urandom(16)
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext) + padder.finalize()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        return iv + ciphertext

    @staticmethod
    def decrypt(ciphertext: bytes, key: bytes) -> bytes:
        iv = ciphertext[:16]
        actual = ciphertext[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(actual) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded) + unpadder.finalize()

    @staticmethod
    def encrypt_keyword(keyword: str, key: bytes) -> str:
        h = hashes.Hash(hashes.SHA256())
        h.update(key + keyword.lower().encode())
        return h.finalize().hex()