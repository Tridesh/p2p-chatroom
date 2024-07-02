import socket 
import threading
import string 
import math

ip_address = '127.0.0.1'
letters = string.ascii_letters
letNumDict, numLetDict = {' ': 0}, {0: ' '}
ind = 1
for l in letters:
    letNumDict[l] = ind
    numLetDict[ind] = l
    ind += 1

choice = input("Do you want to host (1) or join (2): ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_address, 9988))
    server.listen(100)
    client, _ = server.accept()


elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_address, 9988))

else:
    exit()

def send_msg(c):
    while True:
        message = input("")
        encrypted_msg = rsa_encrypt(message)
        c.send(encrypted_msg.encode())
        print("You: " + message)

def rec_msg(c):
    while True:
        encrypted_msg = c.recv(1024).decode()
        decrypted_msg = rsa_decrypt(encrypted_msg)  
        print("Partner: " + decrypted_msg)

def rsa_encrypt(message):
    charIndex = [letNumDict[c] for c in message]
    

    p, q = 3, 11
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 2
    while True:
        if math.gcd(e, phi_n) == 1:
            break
        else:
            e += 1
    
    cipherNums = [(i ** e) % n for i in charIndex]
    encrypted_msg = ''.join(f"{num:02}" for num in cipherNums) 
    
    return encrypted_msg

def rsa_decrypt(encrypted_msg):

    cipherNums = [int(encrypted_msg[i:i+2]) for i in range(0, len(encrypted_msg), 2)]
    

    p, q = 3, 11
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 2
    while True:
        if math.gcd(e, phi_n) == 1:
            break
        else:
            e += 1
    d = 2
    while True:
        if ((e * d) % phi_n) == 1:
            break
        else:
            d += 1
    
    decNums = [(i ** d) % n for i in cipherNums]
    
    decrypted_msg = ''.join(numLetDict[i] for i in decNums)
    
    return decrypted_msg

threading.Thread(target=send_msg, args=(client,)).start()
threading.Thread(target=rec_msg, args=(client,)).start()
