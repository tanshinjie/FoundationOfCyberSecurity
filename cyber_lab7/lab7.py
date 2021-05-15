############################
### Tan Shin Jie 1003715 ###
############################
from Crypto.Signature import PKCS1_PSS
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
import string
import random
import base64
import math

def square_multiply(a, x, n):
    res = 1
    for i in bin(x)[2:]:
        res = res * res % n
        if i == "1":
            res = res * a % n
    return res

def demo_RSA_encryption_decryption():
    print('Part I')
    print('demo_RSA_encryption_decryption')
    public_key_file = open("mykey.pem.pub", "r")
    rsakey = RSA.importKey(public_key_file.read())
    e = rsakey.e
    n = rsakey.n

    message = open('message.txt','r').read()
    print('Message:', open('message.txt','r').read())
    ciphertext = square_multiply(int.from_bytes(message.encode(),byteorder='big'),e,n)
    print('Ciphertext:',hex(ciphertext))
    print()

    private_key_file = open("mykey.pem.priv", "r")
    key = private_key_file.read()
    rsakey = RSA.importKey(key)
    d = rsakey.d
    n = rsakey.n

    decrypted_message = square_multiply(ciphertext,d,n)
    decrypted_message = int.to_bytes(decrypted_message,len(message),byteorder='big').decode()
    print('Decrypted:', decrypted_message)
    print('Decrypted == Message ? ',decrypted_message==message)
    print()

def demo_digital_signature():
    print('Part I')
    print('demo_digital_signature')
    private_key_file = open("mykey.pem.priv", "r")
    rsakey = RSA.importKey(private_key_file.read())
    d = rsakey.d
    n = rsakey.n

    message = open('message.txt','rb').read()

    hashFunc = SHA256.new()
    hashFunc.update(message)
    digest = hashFunc.hexdigest()
    print('Digest:', digest)
    print()

    encrypted_digest = square_multiply(int(digest,16),d,n)
    print('Encrypted digest:', hex(encrypted_digest))
    print()

    public_key_file = open("mykey.pem.pub", "r")
    pubKey = public_key_file.read()
    rsakey = RSA.importKey(pubKey)
    e = rsakey.e
    n = rsakey.n

    decrypted_digest = hex(square_multiply(encrypted_digest,e,n))[2:]
    print('Decrypted digest', decrypted_digest)
    print()
    print('Digest == Decrypted digest ?',decrypted_digest==digest)

def demo_RSA_encryption_decryption_protocol_attack():
    print('\nPart II')
    print('demo_RSA_encryption_decryption_protocol_attack\n')
    public_key_file = open("mykey.pem.pub", "r")
    pubKey = public_key_file.read()
    rsakey = RSA.importKey(pubKey)
    e = rsakey.e
    n = rsakey.n

    message = 100
    print("Encrypting:",message,'\n')

    ciphertext = square_multiply(message,e,n)
    print(ciphertext)
    print("Results",base64.b64encode(int.to_bytes(ciphertext,(ciphertext.bit_length() + 7) // 8, 'little')))

    multiplier_s = 2
    ciphertext_multiplier_s = square_multiply(multiplier_s,e,n)

    m = ciphertext * ciphertext_multiplier_s
    print('Modified to:',base64.b64encode(int.to_bytes(m,(m.bit_length() + 7) // 8, 'little')),'\n')

    private_key_file = open("mykey.pem.priv", "r")
    key = private_key_file.read()
    rsakey = RSA.importKey(key)
    d = rsakey.d
    n = rsakey.n

    decrypted_message = square_multiply(m,d,n)
    print("Decrypted:",decrypted_message)
    print('decrypted_message == message ?',decrypted_message==message)

def demo_digital_signature_protocol_attack():
    print('\nPart II')
    print('demo_digital_signature_protocol_attack')
    public_key_file = open("mykey.pem.pub", "r")
    pubKey = public_key_file.read()
    rsakey = RSA.importKey(pubKey)
    e = rsakey.e
    n = rsakey.n

    random_signature = ''
    for i in range(10):
        random_signature += string.hexdigits[random.randint(0,len(string.hexdigits)-1)]
    random_digest = square_multiply(int.from_bytes(random_signature.encode(),byteorder='big'),e,n)
    print('Random signature:',random_signature)
    print('Digest from random signature:',hex(random_digest))
    print()

    public_key_file = open("mykey.pem.pub", "r")
    pubKey = public_key_file.read()
    rsakey = RSA.importKey(pubKey)
    e = rsakey.e
    n = rsakey.n

    received_random_signature = random_signature
    print('Received signature(random):',received_random_signature)
    digest_from_received_random_signature = square_multiply(int.from_bytes(received_random_signature.encode(),byteorder='big'),e,n)
    print('Digest from received signature(random):',hex(digest_from_received_random_signature))
    print()
    print('Digest from received signature(random) == Digest from random signature ? ',digest_from_received_random_signature==random_digest)

def generate_RSA(name,bits=1024):
    key = RSA.generate(bits)
    public_key_file = open('{}.pem.pub'.format(name),'wb+')
    public_key = key.publickey().exportKey("PEM") 
    public_key_file.write(public_key)

    private_key_file = open('{}.pem.priv'.format(name),'wb+')
    private_key = key.exportKey("PEM") 
    private_key_file.write(private_key)
    return 

def encrypt_RSA(public_key_file,message):
    key = RSA.importKey(open(public_key_file).read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(message)
    return ciphertext

def decrypt_RSA(private_key_file,ciphertext):
    key = RSA.importKey(open(private_key_file).read())
    cipher = PKCS1_OAEP.new(key)
    message = cipher.decrypt(ciphertext)
    return message

def sign_data(private_key_file,message):
    key = RSA.import_key(open(private_key_file).read())
    h = SHA256.new(message)
    signature = PKCS1_PSS.new(key).sign(h)
    return signature

def verify_sign(public_key_file,sign,data):
    key = RSA.import_key(open(public_key_file).read())
    h = SHA256.new(data)
    verifier = PKCS1_PSS.new(key)
    return verifier.verify(h, sign)

def demo_message_exchange():
    print('\nPart III')
    print('Demo: Message exchange between Alice and Bob')
    print('Setting up...:')
    print('Generating secret_message.txt')
    original_message = 'This is a secret message from Alice to Bob'
    with open('secret_message.txt','w+') as f:
        f.write(original_message)

    print('Generating key pairs for Alice and Bob')
    generate_RSA('alice')
    generate_RSA('bob')

    print('Done\n')
    secret_file = 'secret_message.txt'
    alice_public_key_file = 'alice.pem.pub'
    alice_private_key_file = 'alice.pem.priv'
    bob_public_key_file = 'bob.pem.pub'
    bob_private_key_file = 'bob.pem.priv'

    print('Alice wants to send secret_message.txt to Bob')
    print("Alice encrypts the content with Bob's public key")
    alice_message = open(secret_file,'rb').read()
    ciphertext = encrypt_RSA(bob_public_key_file,alice_message)

    print('Alice writes ciphertext to secret_message_enc.txt')
    with open('secret_message_enc.txt','wb+') as f:
        f.write(ciphertext)
    
    signature = sign_data(alice_private_key_file,alice_message)
    print("Alice uses Alice's private key to generate her digital signature and writes to secret_message_digest.txt")
    with open('secret_message_digest.txt','wb+') as f:
        f.write(signature)

    print('Alice sends secret_message_enc.txt and secret_message_digest.txt to Bob\n')
    print("Bob receives the two files from Alice")
    print("Bob decryptes secret_message_enc.txt with Bob's private key")
    encrypted_message = open('secret_message_enc.txt','rb').read()
    decrypted_message = decrypt_RSA(bob_private_key_file,encrypted_message)
    print("Did the decrypted_message match with alice_message?",decrypted_message==alice_message)

    print("Bob verifies the digital signature with Alice's public key")
    received_signature = open('secret_message_digest.txt','rb').read()
    print("Did the message actually comes from Alice?", verify_sign(alice_public_key_file,received_signature,decrypted_message))

if __name__ == "__main__":
    message = open('message.txt','rb').read()
    public_key_file = 'mykey.pem.pub'
    private_key_file = 'mykey.pem.priv'

    print('Test 1: Encryption and Decryption on message')
    ciphertext = encrypt_RSA(public_key_file,message)
    plaintext = decrypt_RSA(private_key_file,ciphertext)
    assert message == plaintext

    print('Test 2: Digital Signature with encryption')
    signature = sign_data(private_key_file,message)
    assert verify_sign(public_key_file,signature,message)
    print()

    demo_RSA_encryption_decryption()
    demo_digital_signature()
    demo_RSA_encryption_decryption_protocol_attack()
    demo_digital_signature_protocol_attack()

    demo_message_exchange()

