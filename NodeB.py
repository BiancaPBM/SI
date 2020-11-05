import socket
import encryptHelper
import struct
#Initialize key K3
k3=b'abcdefghijklmnop'

#initialize the socket and server port where B will listen for incoming connection-> first from KM
sockNodeB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address_b = ('localhost', 2222)
print('\n[NodeB] Starting up on {} port {}'.format(*server_address_b))

#print('[NodeK] Starting up on {} port {}'.format(*server_address_b))
sockNodeB.bind(server_address_b)

# Listen for incoming connections
sockNodeB.listen(1)
conn_b, client = sockNodeB.accept()

#read the message from KM
mode = conn_b.recv(3)
encryptedKey = conn_b.recv(16)
encryptedIV = conn_b.recv(16)
print(encryptedKey,mode,k3)

decryptedKey = encryptHelper.decryptBlock(encryptedKey,mode.decode(),k3,encryptHelper.initVector)
decryptedIV = encryptHelper.decryptBlock(encryptedIV,mode.decode(),k3,encryptHelper.initVector)

print("\nDecripted key is:",decryptedKey)
print("\nDecrypted vector is:", decryptedIV)
encryptedMessage = encryptHelper.encryptBlock(b"Between A and B ",mode.decode(),decryptedKey,decryptedIV)
conn_b.sendall(encryptedMessage)
successMessageFromKM = conn_b.recv(2)
print("\n Message sent by KM in order to see what to do with communication A-B: ",successMessageFromKM.decode())

#accepts A node
conn_a,client_a = sockNodeB.accept()
print('\n[NodeB] Connection with A has been made!')

nrInBytes = conn_a.recv(2)
print(nrInBytes.decode())
numberOfBlocks = int(float(nrInBytes.decode()))
conn_b.sendall(str(numberOfBlocks).encode())
finalDecryptedMessage = ''
while numberOfBlocks > 0:
    block = conn_a.recv(16)
    decrptedMessage = encryptHelper.decryptBlock(block,mode.decode(),decryptedKey,decryptedIV)
    decryptedIV = block
    print("\n Blocs: ",decrptedMessage)
    numberOfBlocks = numberOfBlocks - 1 
    finalDecryptedMessage =finalDecryptedMessage + decrptedMessage.decode()

print("\nMessage from A is: ",finalDecryptedMessage)
conn_a.close()
sockNodeB.close()
