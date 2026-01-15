import base64
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import jwt
import bcrypt  # Use direct bcrypt instead of passlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from backend.app.core.config import settings

# AES-256 Encryption Setup
# Ensure key is valid 32 bytes
try:
    # If key is base64 encoded in env
    ENCRYPTION_KEY_BYTES = base64.urlsafe_b64decode(settings.ENCRYPTION_KEY)
except Exception:
    # Fallback if it's a raw string (needs to be 32 chars/bytes for AES-256)
    # This is a fallback for dev, strictly should be base64 32 bytes.
    # We pad or truncate to 32 bytes for safety in dev (NOT PROD SAFE but avoids crash)
    key_str = settings.ENCRYPTION_KEY
    ENCRYPTION_KEY_BYTES = key_str.encode()[:32].ljust(32, b'0')

if len(ENCRYPTION_KEY_BYTES) != 32:
    # If still not 32, force generation (ephemeral, data loss on restart if used)
    print("WARNING: ENCRYPTION_KEY is not 32 bytes. Using ephemeral key.")
    ENCRYPTION_KEY_BYTES = os.urandom(32)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def encrypt_field(raw_value: str) -> str:
    """
    Encrypts a string using AES-256-GCM.
    Returns format: IV(b64):TAG(b64):CIPHERTEXT(b64)
    """
    if not raw_value:
        return ""
    
    iv = os.urandom(12)  # NIST recommended IV size for GCM
    
    encryptor = Cipher(
        algorithms.AES(ENCRYPTION_KEY_BYTES),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()
    
    ciphertext = encryptor.update(raw_value.encode()) + encryptor.finalize()
    
    return f"{base64.urlsafe_b64encode(iv).decode()}:{base64.urlsafe_b64encode(encryptor.tag).decode()}:{base64.urlsafe_b64encode(ciphertext).decode()}"


def decrypt_field(encrypted_value: str) -> str:
    """
    Decrypts a string. Expects format: IV(b64):TAG(b64):CIPHERTEXT(b64)
    """
    if not encrypted_value or ":" not in encrypted_value:
        return encrypted_value
    
    try:
        parts = encrypted_value.split(":")
        if len(parts) != 3:
            return ""
        
        iv = base64.urlsafe_b64decode(parts[0])
        tag = base64.urlsafe_b64decode(parts[1])
        ciphertext = base64.urlsafe_b64decode(parts[2])
        
        decryptor = Cipher(
            algorithms.AES(ENCRYPTION_KEY_BYTES),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()
        
        return (decryptor.update(ciphertext) + decryptor.finalize()).decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return ""
