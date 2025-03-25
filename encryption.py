from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import hashlib



def encrypt_sha3_384(input_data):
    sha3_384 = hashlib.sha3_384()
    sha3_384.update(input_data.encode('utf-8'))
    hash_bytes = sha3_384.digest()
    base64_encoded = base64.b64encode(hash_bytes)
    return base64_encoded.decode('utf-8')


def encrypt_aes_256(key: bytes, iv: bytes, plaintext: str) -> str:
    # Create a Cipher object using the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plaintext to be a multiple of the block size (16 bytes for AES)
    pad_length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext + (chr(pad_length) * pad_length)

    # Encrypt the padded plaintext
    ciphertext = encryptor.update(padded_plaintext.encode()) + encryptor.finalize()

    # Encode the ciphertext in Base64
    return base64.b64encode(ciphertext).decode()

def decrypt_aes_256(key: bytes, iv: bytes, ciphertext_b64: str) -> str:
    # Decode the Base64 encoded ciphertext
    ciphertext = base64.b64decode(ciphertext_b64)

    # Create a Cipher object using the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    pad_length = padded_plaintext[-1]
    plaintext = padded_plaintext[:-pad_length].decode()

    return plaintext

'''
if __name__ == "__main__":
    # Define a 32-byte key and a 16-byte IV (both should be kept secret)
    key = b'3j4tWPZ2fMQp76h8tZJzLEncISewefwe'  # 32 bytes for AES-256
    iv = b'ztF22CY+qRZeTd09'             # 16 bytes for IV

    # Text to encrypt
    plaintext = "Hello, World!!"

    # Encrypt the plaintext
    encrypted_output = encrypt_aes_256(key, iv, plaintext)
    print("Encrypted (Base64):", encrypted_output)

    # Decrypt the ciphertext
    decrypted_output = decrypt_aes_256(key, iv, encrypted_output)
    print("Decrypted:", decrypted_output)
'''
#print(encrypt_sha3_384('test'))

def genencryptionkey(inputkey):
    key = encrypt_sha3_384(inputkey)
    return key

def encryptwithkey(key, data):
    key=str(key)
    #nameoffile = key[0:16]
    keyenc = key[16:48].encode('utf-8')
    iv = key[48:].encode('utf-8')
    encrypted_output = encrypt_aes_256(keyenc, iv, data)
    #output = [encrypted_output]
    return encrypted_output

def decryptwithkey(key, data):
    key=str(key)
    #nameoffile = key[0:16]
    keyenc = key[16:48].encode('utf-8')
    iv = key[48:].encode('utf-8')
    decrypted_output = decrypt_aes_256(keyenc, iv, data)
    #output = [decrypted_output]
    return decrypted_output


