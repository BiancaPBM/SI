from Crypto import Random
from Crypto.Cipher import AES
import binascii

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]
initVector = b'aabbccddeeffgghh'

def generateRandom16bytes():
    return Random.get_random_bytes(16)


def encryptBlock(block, mode, key,iv):
    encryptedBlock = 0
    if mode == "CBC":
        modeType = AES.MODE_CBC        
        x = xor(block,iv)
        aesObj = AES.new(key,modeType)
        encryptedBlock = aesObj.encrypt(x)
    elif mode == "CFB":
        modeType = AES.MODE_CFB
        aesObj = AES.new(key,modeType)
        encryptedIv = aesObj.encrypt(iv)
        encryptedBlock = xor(block,encryptedIv)

    return encryptedBlock

def decryptBlock(block, mode, key,iv):
    if mode == "CBC":
        modeType = AES.MODE_CBC
        aesObj = AES.new(key,modeType)
        decryptedBlock = aesObj.decrypt(block)
        plainText = xor(decryptedBlock,iv)
    elif mode == "CFB":
        modeType = AES.MODE_CFB
        aesObj = AES.new(key,modeType)
        cypherEncryption = aesObj.encrypt(iv)
        plainText = xor(block,cypherEncryption)

    return plainText

def xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def  encryptBlock1(block, mode, key,iv):
     if mode == "CBC":
        modeType = AES.MODE_CBC        
     elif mode == "CFB":
        modeType = AES.MODE_CFB
    
     aesObj = AES.new(key,modeType,iv)
     encryptedBlock = aesObj.encrypt(block)
     return encryptedBlock

def  decryptBlock1(block, mode, key,iv):
     if mode == "CBC":
        modeType = AES.MODE_CBC        
     elif mode == "CFB":
        modeType = AES.MODE_CFB
    
     aesObj = AES.new(key,modeType,iv)
     decryptedBlock = aesObj.decrypt(block)
     return decryptedBlock

