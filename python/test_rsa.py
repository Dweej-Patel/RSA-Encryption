from rsa import RSA_Encrypt

bit_enc = input("Enter the number of bits encryption to perform: ")

# Get bit_enc bit RSA encrytion
rsa_encryption = RSA_Encrypt(int(bit_enc))

# Generate keys
rsa_encryption.generate_encryption()

# Get public key and mod number to send
send = rsa_encryption.send_public_key()

# Display public key and mod number
print("\n")
print("Public Key: \n" + str(send['public_key']))
print("\n")
print("Private Key: \n" + str(rsa_encryption._RSA_Encrypt__private_key))
print("\n")
print("Modulo N: \n" + str(send['mod']))
print("\n")

# Enter message until you type exit
message = input("Enter message you want to encrypt: \n")
while message != 'quit':
    encrypted = rsa_encryption.encrypt_message(message, send['public_key'], send['mod'])
    print("\n")
    print("Your encrypted message: \n" + str(encrypted))
    decrypted = rsa_encryption.decrypt_message(encrypted)
    print("\n")
    print("Your message should be the same after decryption: \n" + decrypted)
    print("\n")
    message = input("Enter another message (Enter 'quit' to exit): \n")
print("\n")