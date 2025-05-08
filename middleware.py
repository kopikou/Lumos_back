# from cryptography.fernet import Fernet
# import base64
# import json

# class DecryptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.key = b'LumosEncryptionKey'  # Должен совпадать с ключом на клиенте
#         self.cipher = Fernet(base64.urlsafe_b64encode(self.key))

#     def __call__(self, request):
#         if request.path == '/api/token/' and request.method == 'POST':
#             try:
#                 data = json.loads(request.body)
#                 if 'password' in data:
#                     encrypted = data['password'].split(':')
#                     iv = base64.b64decode(encrypted[0])
#                     encrypted_data = base64.b64decode(encrypted[1])
#                     data['password'] = self._decrypt(iv, encrypted_data)
#                     request._body = json.dumps(data).encode('utf-8')
#             except Exception as e:
#                 print(f"Decryption error: {e}")
        
#         return self.get_response(request)
    
#     def _decrypt(self, iv, encrypted_data):
#         # Реализация расшифровки
#         return self.cipher.decrypt(encrypted_data).decode()
# import base64
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# from django.utils.deprecation import MiddlewareMixin

# # Конкретный ключ нужно хранить безопасным способом, не передавать его открытым текстом
# SECRET_KEY = b'LumosEncryptionKey'  # Сюда подставляете свой ключ

# def decrypt_data(encoded_data):
#     """ Функция для расшифровки данных. Входящие данные состоят из двух частей: IV и зашифрованного контента. Данные передаются в виде строки, разделённые ":" """
#     parts = encoded_data.split(':', maxsplit=1)
#     if len(parts) != 2:
#         raise ValueError("Invalid data format.")

#     iv_base64, ciphertext_base64 = parts
#     iv = base64.b64decode(iv_base64)
#     ciphertext = base64.b64decode(ciphertext_base64)

#     backend = default_backend()
#     cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=backend)
#     decryptor = cipher.decryptor()
#     decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

#     # PKCS7 padding (Python's Cryptography package handles it automatically when decryption happens)
#     return decrypted_padded.decode('utf-8').strip()

# class DecryptionMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         """ Декоратор запроса для дешифрования данных. Предположим, что данные находятся в теле POST-запроса. """
#         if request.method == 'POST':
#             body = request.body.decode('utf-8')  # Получаем сырые данные из тела запроса
#             try:
#                 decrypted_body = decrypt_data(body)
#                 request._body = decrypted_body.encode('utf-8')  # Замещаем исходное тело на расшифрованное
#             except Exception as e:
#                 print(f"Decryption failed: {e}")  # Логируем ошибки
#                 pass  # Можно вернуть ошибку клиенту или продолжить работу без расшифровки

#     def process_response(self, request, response):
#         """Опционально можно реализовать шифрование ответа."""
#         return response


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import json

class DecryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Симметричный ключ (должен соответствовать вашему клиенту!)
        self.secret_key = base64.urlsafe_b64decode(b'AwRxf_B-vjrdCxIKguThJeEVhcyPYkjiimcZyrMBRDA=')  # Приведите сюда действительный 32-байтовый ключ

    def __call__(self, request):
        if request.path == '/api/token/' and request.method == 'POST':
            try:
                data = json.loads(request.body)
                if 'password' in data:
                    encrypted_parts = data['password'].split(':')
                    if len(encrypted_parts) != 2:
                        raise ValueError("Encrypted data has invalid format")
                    
                    iv = base64.b64decode(encrypted_parts[0])
                    encrypted_data = base64.b64decode(encrypted_parts[1])

                    # Декодируем данные с использованием AES-CBC
                    backend = default_backend()
                    cipher = Cipher(algorithms.AES(self.secret_key), modes.CBC(iv), backend=backend)
                    decryptor = cipher.decryptor()
                    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

                    # Автоматическое снятие дополнения PKCS7
                    unpadded_data = decrypted_padded.strip(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f')

                    data['password'] = unpadded_data.decode('utf-8')
                    request._body = json.dumps(data).encode('utf-8')
            except Exception as e:
                print(f"Decryption error: {e}")
        
        return self.get_response(request)