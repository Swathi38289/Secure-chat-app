from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

def generate_rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()

# --- NEW: Helper to save Private Keys locally ---
def serialize_private_key(private_key):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def load_public_key(pem_data):
    # Standardizing to handle both string and bytes
    if isinstance(pem_data, str):
        pem_data = pem_data.encode('utf-8')
    return serialization.load_pem_public_key(pem_data)

def encrypt_message(message):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    # Using explicit utf-8 encoding
    return key, cipher.encrypt(message.encode('utf-8'))

def encrypt_key(aes_key, public_key):
    return public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), 
            algorithm=hashes.SHA256(), 
            label=None
        )
    )

def decrypt_key(encrypted_key, private_key):
    try:
        return private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                algorithm=hashes.SHA256(), 
                label=None
            )
        )
    except Exception as e:
        print(f"Decryption Key Error: {e}")
        return None

def decrypt_message(encrypted_msg, aes_key):
    try:
        return Fernet(aes_key).decrypt(encrypted_msg).decode('utf-8')
    except Exception as e:
        print(f"Decryption Message Error: {e}")
        return "[Error: Decryption Failed]"