from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from os.path import expanduser
import configparser
import getpass


# awsconfigfile: The file where this script will store the temp
# credentials under the saml profile
home = expanduser("~")

awsconfigfile = home + '/.aws/config'
password_file = home + '/.aws/secret'

# Read in the existing config file
config = configparser.RawConfigParser()
config.read(awsconfigfile)

print("Full path to your PEM file:")
pemfile = input()
recipient_key = RSA.import_key(open(pemfile).read())


print("Password:")
password = getpass.getpass()

file_out = open(password_file, "wb")

session_key = get_random_bytes(16)

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(password.encode())
[ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]

if not config.has_section('samlapi'):
    config.add_section('samlapi')

config.set('samlapi', 'pemfile', pemfile)
config.set('samlapi', 'password_file', password_file)

# Write the updated config file
with open(awsconfigfile, 'w+') as configfile:
    config.write(configfile)

print('Configuration updated.')