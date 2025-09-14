from Crypto.Cipher import AES
import hashlib
import os

def pad(data):
    padding_length = 16 - len(data) % 16
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad(data):
    padding_length = data[-1]
    if padding_length < 1 or padding_length > 16:
        raise ValueError("Invalid padding encountered")
    return data[:-padding_length]

def encrypt_file(input_file, output_file, password):
    zero = 0
    iv = zero.to_bytes(16, 'big')
    key = bytearray(hashlib.sha256(password.encode()).digest())
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        with open(input_file, 'rb') as f:
            plaintext = f.read()
        padded_plaintext = pad(plaintext)
        ciphertext = cipher.encrypt(padded_plaintext)
        with open(output_file, 'wb') as f:
            f.write(ciphertext)
        encoded_key = key.hex()
        encoded_iv = iv.hex()
        return encoded_key, encoded_iv
    except Exception as e:
        return None, None
    
def decrypt_file(input_file, output_file, password):
    zero = 0
    iv = zero.to_bytes(16, 'big')
    key = bytearray(hashlib.sha256(password.encode()).digest())
    try:
        if len(key) != 32:
            raise ValueError("Incorrect AES key length")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = unpad(cipher.decrypt(encrypted_data))
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
    except Exception as e:
        print(f"An error occurred during decryption: {e}")

decrypt_file("locker.csv", "locker.csv", "banana")