from cryptography.fernet import Fernet


def encrypt(text):
    crypto = init_crypto()

    text = text if isinstance(text, str) else str(text)  # Text must be str
    encoded_message = text.encode()

    return {
        'encryptedValue': crypto.encrypt(encoded_message).decode("utf-8")
    }


def decrypt(encrypted_message):
    crypto = init_crypto()

    encrypted_message = encrypted_message if isinstance(encrypted_message, bytes) else encrypted_message.encode()
    decrypted_message = crypto.decrypt(encrypted_message)

    return {
        'decryptedValue': decrypted_message.decode()
    }


def init_crypto():
    KEY = 'ydy-_amv$igor0+!r7n8(l+f@i2&1w1t(gki6d7bzdrbq9d0y='
    return Fernet(KEY)
