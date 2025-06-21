from Crypto.Cipher import AES
import base64
import hashlib

def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

def encrypt_text(plain_text, password):
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(plain_text).encode())
    return base64.b64encode(encrypted).decode()

def decrypt_text(cipher_text, password):
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(cipher_text.encode()))
    return decrypted.decode().strip()
