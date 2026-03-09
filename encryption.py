from pathlib import Path
from cryptography.fernet import Fernet

KEY_FILE = Path("secret.key")


def load_or_create_key():
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()

    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    return key


def get_cipher():
    key = load_or_create_key()
    return Fernet(key)


def encrypt_password(password: str) -> str:
    cipher = get_cipher()
    encrypted = cipher.encrypt(password.encode("utf-8"))
    return encrypted.decode("utf-8")


def decrypt_password(encrypted_password: str) -> str:
    cipher = get_cipher()
    decrypted = cipher.decrypt(encrypted_password.encode("utf-8"))
    return decrypted.decode("utf-8")