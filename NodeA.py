import socket
import encryptHelper
from Crypto.Util.Padding import pad
#Initialize key K3
k3=b'abcdefghijklmnop'

# Create a TCP/IP socket
sockNodeKM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address_km = ('localhost', 1337)
print('\n Step 1:[NodeA] Connecting to {} port {}'.format(*server_address_km))

#Connect to KM node
sockNodeKM.connect(server_address_km)

#choose mode and send it to KM
print("\nChoose encryption mode(CBC/CFB): ")
mode = input().upper()
while not (mode == "CBC" or mode == "CFB"):
    print("You mispelled one of the encryption mode, or we not support the encryption you want\n Please, write again: ")
    mode = input().upper()

print("You chose encryption mode ", mode, " !")
binMode= str.encode(mode)
#print (binMode)
sockNodeKM.sendall(binMode)

#receive encrypted key from km
encryptedKey = sockNodeKM.recv(16)
initializedVector = sockNodeKM.recv(16)
#decrypt key
decryptedKey = encryptHelper.decryptBlock(encryptedKey,mode,k3,encryptHelper.initVector)
print("\nDecrypted key is:", decryptedKey)
decryptedVector = encryptHelper.decryptBlock(initializedVector,mode,k3,encryptHelper.initVector)
print("\nDecrypted vector is:", decryptedVector)

#encrypt block with the new decrypted key and send it to KM
encryptedBlock = encryptHelper.encryptBlock(b"Between A and B ",mode,decryptedKey, decryptedVector)
sockNodeKM.sendall(encryptedBlock)

#receive message from KM in order to continue communication
messageForCommunication = sockNodeKM.recv(2)
print("\nMessage sent by KM in order to see what to do with communication A-B: ",messageForCommunication.decode())
sockNodeB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address_b = ('localhost', 2222)
print('\n[NodeA] Connecting to {} port {}'.format(*server_address_b))
if messageForCommunication == b"Ok":
    f = open("file.txt", "r")
    messageFromFile = f.read()
    print("\nMessage from file is:",messageFromFile)
    nrOfBlocks = len(messageFromFile) / encryptHelper.blockSize
    if nrOfBlocks > int(nrOfBlocks):
      nrOfBlocks = nrOfBlocks + 1
    #connect to B
    sockNodeB.connect(server_address_b)

    # send to km the number of blocks cripted
    sockNodeB.sendall(str(int(nrOfBlocks)).encode())
    sockNodeKM.sendall(str(int(nrOfBlocks)).encode())
    i = 0
    pos = 0
    while i < int(nrOfBlocks):
        block = messageFromFile[pos: pos + encryptHelper.blockSize]
        pos = pos + encryptHelper.blockSize
        if int(nrOfBlocks) - i == 1:
            block = pad(block.encode(),16).decode()
        #print("Block is:", block)
        enctyptedMessage = encryptHelper.encryptBlock(block.encode(),mode,decryptedKey,decryptedVector)
        sockNodeB.sendall(enctyptedMessage)
        decryptedVector = enctyptedMessage
        i = i + 1
    
    sockNodeB.close()
    sockNodeKM.close()


    