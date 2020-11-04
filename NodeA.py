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
mode = input()
print (mode)
binMode= str.encode(mode)
print (binMode)
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
encryptedBlock = encryptHelper.encryptBlock(b"AAAABBBBCCCCDDDD",mode,decryptedKey, decryptedVector)
sockNodeKM.sendall(encryptedBlock)

#receive message from KM in order to continue communication
messageForCommunication = sockNodeKM.recv(2)
print("\nMessage for communication is: ",messageForCommunication)
if messageForCommunication == b"Ok":
    f = open("file.txt", "r")
    messageFromFile = f.read()
    print("\nMessage from file is:",messageFromFile)
    enctyptedMessage = encryptHelper.encryptBlock(messageFromFile.encode(),mode,decryptedKey,decryptedVector)
    print("\nEncrypted message for communication is: ",enctyptedMessage)

    # send to km the number of blocks cripted
    sockNodeKM.sendall(enctyptedMessage)
    
    #send to B cripted message

    # Create a TCP/IP socket
    sockNodeB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address_b = ('localhost', 2222)
    print('\n[NodeA] Connecting to {} port {}'.format(*server_address_b))

    #Connect to b node
    sockNodeB.connect(server_address_b)   
    sockNodeB.sendall(enctyptedMessage)

    sockNodeB.close()
    sockNodeKM.close()


    