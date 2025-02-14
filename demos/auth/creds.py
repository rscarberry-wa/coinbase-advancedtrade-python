import os
import json
import base64
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
from getpass import getpass


# Encrypt a file using AES-256
def encrypt_file(input_file, output_file, password):
    # Generate a random 16-byte (128-bit) salt
    salt = os.urandom(16)

    # Derive a key using PBKDF2HMAC with the supplied password and the salt
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 requires a 32-byte key
        salt=salt,
        iterations=100000,  # Increase iterations for stronger protection
        backend=backend
    )
    key = kdf.derive(password.encode())

    # Generate a random 16-byte initialization vector (IV)
    iv = os.urandom(16)

    # Prepare the AES cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    # Read the input file and pad it using PKCS7 padding
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Encrypt the padded plaintext
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Save the salt, IV, and ciphertext to the output file in base64 encoding
    with open(output_file, 'wb') as f:
        f.write(base64.b64encode(salt + iv + ciphertext))

def decrypt_to_dict(encrypted_file_path, password):
    """
    Decrypts an AES-256 encrypted file and loads its contents as a dictionary.

    Args:
        encrypted_file_path (str): The path to the encrypted file.

    Returns:
        dict: The contents of the decrypted file as a dictionary.
    """
    try:
        # Check if the file exists
        if not os.path.exists(encrypted_file_path):
            raise FileNotFoundError(f"File '{encrypted_file_path}' not found.")

        # Read the encrypted file
        with open(encrypted_file_path, 'rb') as f:
            encrypted_data = base64.b64decode(f.read())

        # Extract the salt, IV, and ciphertext
        salt = encrypted_data[:16]  # First 16 bytes are the salt
        iv = encrypted_data[16:32]  # Next 16 bytes are the IV
        ciphertext = encrypted_data[32:]  # Remaining bytes are the ciphertext

        # Key derivation using PBKDF2HMAC
        backend = default_backend()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256 requires a 32-byte key
            salt=salt,
            iterations=100000,  # Must match the encryption setup
            backend=backend
        )
        key = kdf.derive(password.encode())

        # Prepare the AES cipher in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()

        # Decrypt the ciphertext
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove PKCS7 padding from the plaintext
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        # Convert the plaintext (JSON string) into a Python dictionary
        decrypted_dict = json.loads(plaintext.decode('utf-8'))

        return decrypted_dict

    except Exception as e:
        print(f"Error during decryption: {e}")
        return None

def encrypt_main():
    input_file = "../../.creds/creds.json"
    output_file = "../../../.creds/creds.enc"

    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return

    # Prompt the user for a password
    password = input("Enter a password to encrypt the file: ")

    print("Encrypting the file...")
    try:
        encrypt_file(input_file, output_file, password)
        print(f"Encryption successful. Encrypted file saved as: {output_file}")
    except Exception as e:
        print(f"Error during encryption: {e}")

def decrypt_creds():
    input_file = "../../.creds/creds.enc"
    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return

    # Prompt the user for a password
    password = getpass("Enter a password to decrypt the file: ")
    return decrypt_to_dict(input_file, password)

if __name__ == "__main__":
    print(decrypt_creds())
