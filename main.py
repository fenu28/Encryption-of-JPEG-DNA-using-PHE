import crypton
import rabinMiller
import random
import paillier
from conflictfree import ConflictFree


def binaryToDecimal(str):
    # print(str)
    ans = 0
    k = len(str) - 1
    for i in range(len(str)):
        ans = ans + pow(2, k) * (int(str[i]))
        k = k - 1
    return ans


def fileToBinary(file):
    binaryMapping = {}
    binaryMapping['A'] = "00"
    binaryMapping['C'] = "01"
    binaryMapping['G'] = "10"
    binaryMapping['T'] = "11"
    binary = ""
    with open(file, 'r') as f:
        data = f.read()
        for i in range(len(data)):
            binary = binary + binaryMapping[data[i]]
    return binary


def binaryToDNA(binary):
    dnaMapping = {}
    dnaMapping["00"] = "A"
    dnaMapping["01"] = "C"
    dnaMapping["10"] = "G"
    dnaMapping["11"] = "T"

    dna = ""
    for i in range(0, len(binary), 2):
        block = binary[i] + binary[i + 1]
        dna = dna + dnaMapping[block]
    return dna


def decimalToBinary(decimal: int):
    binary = ""
    if decimal == 0:
        return "0000"
    while (decimal):
        binary = binary + str(decimal & 1)
        decimal = decimal >> 1
    binary = binary[::-1]

    if len(binary) == 1:
        return "000" + binary
    elif len(binary) == 2:
        return "00" + binary
    elif len(binary) == 3:
        return "0" + binary
    else:
        return binary

def decimalToBinary2(decimal):
    if decimal == 0:
        return "00"
    elif decimal == 1:
        return "01"
    elif decimal == 2:
        return "10"
    elif decimal == 3:
        return "11"

def binaryToCipher(binary):
    cipher = ""
    for i in range(0,len(binary),4):
        binaryTemp = "" + str(binary[i]) + str(binary[i + 1]) + str(binary[i + 2]) + str(binary[i + 3])
        decimal = binaryToDecimal(binaryTemp)
        cipher = cipher + str(decimal)
    return cipher


def main():
    p = paillier.Paillier()
    p.generateKey()
    # c = p.encrypt(5)
    # print(c)
    # original = p.decrypt(c)
    # print(original)
    fileName = 'data.txt'
    binary = fileToBinary(fileName)
    decimal = ""
    for i in range(0, len(binary) - 1, 2):
        decimal = decimal + str(binaryToDecimal(str(binary[i]) + str(binary[i + 1])))

    encryptedBinary = 'encryptedBinary.txt'
    encryptedDNA = 'encryptedDNA.txt'
    encrypted = []
    for i in range(len(decimal)):
        encrypted.append(p.encrypt(int(decimal[i])))
        #print(encrypted[i])
        cipher = str(encrypted[i])
        binCipher = ""
        for j in range(len(cipher)):
            binCipher = binCipher + decimalToBinary(int(cipher[j]))
        conflictfreeObj = ConflictFree(binCipher,"")
        conflictfreeObj.encode()
        encoded = conflictfreeObj.dna
        with open(encryptedDNA,'a') as f:
            f.write(encoded+'\n')

    dnaString = []
    with open('encryptedDNA.txt','r') as f:
        dnaString = f.readlines()

    for x in range(len(dnaString)):
        dnaString[x] = dnaString[x].removesuffix('\n')

    decodedBinary = []
    for i in range(len(dnaString)):
        dna = dnaString[i]
        conflictfreeObj = ConflictFree("",dna)
        conflictfreeObj.decode()
        binary = conflictfreeObj.binary
        decodedBinary.append(binary)

    decodedCipherText = []
    for i in range(len(decodedBinary)):
        binary = decodedBinary[i]
        decodedCipher = binaryToCipher(binary)
        decodedCipherText.append(decodedCipher)

    initialBinary = ""
    for i in range(len(decodedCipherText)):
        cipherText = decodedCipherText[i]
        decryptedDecimal = p.decrypt(int(cipherText))
        initialBinary = initialBinary + decimalToBinary2(int(decryptedDecimal))

    originalFile = "decodedFile.txt"
    with open(originalFile,'a') as f:
        for i in range(0,len(initialBinary),2):
            binary = str(initialBinary[i])+str(initialBinary[i+1])
            f.write(binaryToDNA(binary))
    f.close()

    # cipher = binaryToCipher('encryptedBinary.txt')
    # cipherOriginal = []
    # for i in range(len(cipher)):
    #     cipherOriginal.append(int(cipher[i]))
    #
    # cipherBin = decimalToBinary()




main()
