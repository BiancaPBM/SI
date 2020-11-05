import socket
import sys
from Crypto.Cipher import AES
import encryptHelper 


#Initialize keys and vector
k1 = encryptHelper.generateRandom16bytes()
k2 = encryptHelper.generateRandom16bytes()
k3=b'abcdefghijklmnop'
initializedVector = encryptHelper.generateRandom16bytes()
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 1337)
print('\n[NodeKM] Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
phaseOneIsFulfilled = False

#Wait for a connection
# print('[NodeK] Waiting for a connection...')
connectionA, client_address = sock.accept()

#receive specific node connection
    
#Receive mode from node A
mode = connectionA.recv(3)       
if mode == b'CBC':
    #use key1 for cbc
    key = k1
elif mode == b'CFB': 
    #use key2 for cfb
    key = k2
        
encryptedKey = encryptHelper.encryptBlock(key,mode.decode(), k3, encryptHelper.initVector)
encryptedIV = encryptHelper.encryptBlock(initializedVector,mode.decode(), k3,encryptHelper.initVector)
decryptedKey = encryptHelper.encryptBlock(encryptedIV,mode.decode(),k3,encryptHelper.initVector)

#send the encrypted key and initialized vector to A
connectionA.sendall(encryptedKey)
connectionA.sendall(encryptedIV)

messageFromA  = connectionA.recv(16)
    
#print("\nencrypted key is: ",encryptedKey)
decryptedMessageFromA = encryptHelper.decryptBlock(messageFromA, mode.decode(),key,initializedVector)
#print("\ndecrypred key is:", decryptedKey)
#print("\nDecrypted message from A is: ",decryptedMessageFromA)

#bind to node B
sockNodeB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address_b = ('localhost', 2222)
print('\n[NodeKM] Connecting to {} port {}'.format(*server_address_b))
sockNodeB.connect(server_address_b)
    
#send to B mode and encrypted key
sockNodeB.sendall(mode)
sockNodeB.sendall(encryptedKey)
sockNodeB.sendall(encryptedIV)
encryptedMessageFromB = sockNodeB.recv(16)
decryptedMessageFromB = encryptHelper.decryptBlock(encryptedMessageFromB,mode.decode(),key,initializedVector)
#print("\nlet's see the result")
if decryptedMessageFromA == decryptedMessageFromB:
    print("\nOk")
    connectionA.sendall(b"Ok")
    sockNodeB.sendall(b"Ok")
else:
        print("NOT OK")
blocksFromA = connectionA.recv(16)
blocksFromB = sockNodeB.recv(16)
print("\nBlocks from A:",blocksFromA.decode())
print("\nBlocks from B:",blocksFromB.decode())


connectionA.close()
sockNodeB.close()
