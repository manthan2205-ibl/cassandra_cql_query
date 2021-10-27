from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import status, exceptions
from . models import *


def Authenticate(self, request):
    auth = get_authorization_header(request).split()
    if not auth or auth[0].lower() != b'token':
        return None

    if len(auth) == 1:
        msg = 'Invalid token header. No credentials provided.'
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = 'Invalid token header'
        raise exceptions.AuthenticationFailed(msg)

    try:
        token = auth[1]
        if token == "null":
            msg = 'Null token not allowed'
            raise exceptions.AuthenticationFailed(msg)
    except UnicodeError:
        msg = 'Invalid token header. Token string should not contain invalid characters.'
        raise exceptions.AuthenticationFailed(msg)

    return token


from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    print(response)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status'] = response.status_code
        if response.data.get('detail'):
            response.data['message'] = response.data['detail'] 
            response.data.pop("detail")
        response.data['results'] = {}
        
        print(response.data)
    # else:
    #     return Response(
    #         data={
    #             "status":status.HTTP_200_OK,
    #             "message":f"team list",
    #             "results": "team_list"},
    #         status=status.HTTP_200_OK
    #     )

    return response



from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from base64 import b64decode, b64encode


backend = default_backend()
# padder = padding.PKCS7(256).padder()
# unpadder = padding.PKCS7(256).unpadder()


key = b64decode('heyFrj+egrMgWrt+hr//uhEFgbfEf/erFSEhbrphthw=')
iv = b64decode('YmRocm9xc3JlcG16ZGVoZQ==')

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

def data_encryptor(data):
    data = data.encode('utf-8')
    padder = padding.PKCS7(128).padder()
    data = padder.update(data) + padder.finalize()
    encryptor = cipher.encryptor()
    ct = encryptor.update(data) + encryptor.finalize()
    ct_out = b64encode(ct)
    print(ct_out)

    return ct_out


def data_decryptor(data):
    data = b64decode(data)
    unpadder = padding.PKCS7(128).unpadder()
    decryptor = cipher.decryptor()
    plain = decryptor.update(data) + decryptor.finalize()
    plain = unpadder.update(plain) + unpadder.finalize()
    plain = plain.decode("utf-8") 
    print(plain)
    
    return plain



# from cassandra_demo import settings
# import os
# from django.conf import settings

# database = settings.DATABASES
# # print('database', database)

# cassandra = database['cassandra']
# # print('cassandra', cassandra)
# NAME = cassandra['NAME']
# print('NAME', NAME)

# settings.DATABASES['cassandra']['NAME'] = 'new_database'
# if not settings.configured:
#     settings.configure(DEBUG=False)
#     print('NAME', NAME)
# settings.configure(DEBUG=False)

# print('NAME', NAME)
# def new_database():
    
#     database_id = user.username #just something unique
#     newDatabase = {}
#     newDatabase["id"] = database_id
#     newDatabase['ENGINE'] = 'django.db.backends.sqlite3'
#     newDatabase['NAME'] = '/path/to/db_%s.sql' % database_id
#     newDatabase['USER'] = ''
#     newDatabase['PASSWORD'] = ''
#     newDatabase['HOST'] = ''
#     newDatabase['PORT'] = ''
#     settings.DATABASES[database_id] = newDatabase
#     save_db_settings_to_file(newDatabase)


# def save_db_settings_to_file(db_settings):
#     path_to_store_settings = "/path/to/your/project/YOUR_PROJECT_NAME/database_settings/"
#     newDbString = """
#     DATABASES['%(id)s'] = {
#     'ENGINE': '%(ENGINE)s', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#     'NAME': '%(NAME)s',                      # Or path to database file if using sqlite3.
#     'USER': '',                      # Not used with sqlite3.
#     'PASSWORD': '',                  # Not used with sqlite3.
#     'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#     'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#         }
#     """ % db_settings
#     file_to_store_settings = os.path.join(path_to_store_settings, db_settings['id'] + ".py")
#     write_file(file_to_store_settings, newDbString) #psuedocode for compactness













# from rest_framework import pagination
# from rest_framework.response import Response

# class CustomPagination(pagination.PageNumberPagination):
#     def get_paginated_response(self, data):
#         return Response({
#             "status": 200,
#             "message": "Your list",
#             'results':{'data':{ 
#                         'links': {
#                             'next': self.get_next_link(),
#                             'previous': self.get_previous_link()
#                         },
#                         'count': self.page.paginator.count,
#                         'results': data}}
#             })



# from Crypto.Cipher import AES
# from Crypto.Util import Counter
# from Crypto import Random
# import binascii
# import math, random, string

# # AES supports multiple key sizes: 16 (AES128), 24 (AES192), or 32 (AES256).
# key_bytes = 32
# # key = 'c6b93o&ux3dueq3&=wtv8fkp7(g@l%^fl6a(409)$rybb'
# letters = string.ascii_letters
# key = ''.join(random.choice(letters) for i in range(32))

# # Takes as input a 32-byte key and an arbitrary-length plaintext and returns a
# # pair (iv, ciphtertext). "iv" stands for initialization vector.
# def encrypt(key, plaintext):
#     assert len(key) == key_bytes

#     # Choose a random, 16-byte IV.
#     iv = Random.new().read(AES.block_size)

#     # Convert the IV to a Python integer.
#     iv_int = int(binascii.hexlify(iv), 16) 

#     # Create a new Counter object with IV = iv_int.
#     ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)

#     # Create AES-CTR cipher.
#     aes = AES.new(key, AES.MODE_CTR, counter=ctr)

#     # Encrypt and return IV and ciphertext.
#     ciphertext = aes.encrypt(plaintext)
#     return (iv, ciphertext)

# # Takes as input a 32-byte key, a 16-byte IV, and a ciphertext, and outputs the
# # corresponding plaintext.
# def decrypt(key, iv, ciphertext):
#     assert len(key) == key_bytes

#     # Initialize counter for decryption. iv should be the same as the output of
#     # encrypt().
#     iv_int = int(iv.encode('hex'), 16) 
#     ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)

#     # Create AES-CTR cipher.
#     aes = AES.new(key, AES.MODE_CTR, counter=ctr)

#     # Decrypt and return the plaintext.
#     plaintext = aes.decrypt(ciphertext)
#     return plaintext

# (iv, ciphertext) = encrypt(key, 'hella')

# print('iv',iv,'ciphertext', ciphertext)
# print(decrypt(key, iv, ciphertext))