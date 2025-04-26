import hashlib
import base64
from cryptography.fernet import Fernet

def generate_key(password):
    """สร้าง cryptographic key จากรหัสผ่าน"""
    salt = b'fixed_salt_123'  # ใน production ควรใช้ salt ที่สุ่มและเก็บอย่างปลอดภัย
    kdf = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return Fernet(base64.urlsafe_b64encode(kdf))