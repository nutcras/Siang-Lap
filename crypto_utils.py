import hashlib
import base64
from cryptography.fernet import Fernet
import os

def generate_key(password):
    """สร้าง cryptographic key จากรหัสผ่าน"""
    salt = os.getenv('CRYPTO_SALT', 'fixed_salt_123').encode('utf-8')
    kdf = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return Fernet(base64.urlsafe_b64encode(kdf))