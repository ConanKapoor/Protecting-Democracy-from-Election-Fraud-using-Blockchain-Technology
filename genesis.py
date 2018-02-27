################################################################################
# Author - Shivam Kapoor (mailme@shivamkapoor.me)
#
# Implementation for "Protecting Democracy from Election
# Fraud using Blockchain Technology"
#
# Github : https://github.com/ConanKapoor/Protecting-Democracy-from
# -Election-Fraud-using-Blockchain-Technology
################################################################################

import hashlib
import time

class Block:
    def __init__(self, index, previousHash, timestamp, data, currentHash):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.currentHash = currentHash

def getGenesisBlock():
    return Block(0, '0', '1496518102.896031', "My very first block :)", '0q23nfa0se8fhPH234hnjldapjfasdfansdf23')

blockchain = [getGenesisBlock()]

def calculateHash(index, previousHash, timestamp, data):
    value = str(index) + str(previousHash) + str(timestamp) + str(data)
    sha = hashlib.sha256(value.encode('utf-8'))
    return str(sha.hexdigest())

def calculateHashForBlock(block):
    return calculateHash(block.index, block.previousHash, block.timestamp, block.data)

def getLatestBlock():
    return blockchain[len(blockchain)-1]

def generateNextBlock(blockData):
    previousBlock = getLatestBlock()
    nextIndex = previousBlock.index + 1
    nextTimestamp = time.time()
    nextHash = calculateHash(nextIndex, previousBlock.currentHash, nextTimestamp, blockData)
    return Block(nextIndex, previousBlock.currentHash, nextTimestamp, nextHash)

def isSameBlock(block1, block2):
    if block1.index != block2.index:
        return False
    elif block1.previousHash != block2.previousHash:
        return False
    elif block1.timestamp != block2.timestamp:
        return False
    elif block1.data != block2.data:
        return False
    elif block1.currentHash != block2.currentHash:
        return False
    return True

def isValidNewBlock(newBlock, previousBlock):
    if previousBlock.index + 1 != newBlock.index:
        print('Indices Do Not Match Up')
        return False
    elif previousBlock.currentHash != newBlock.previousHash:
        print("Previous hash does not match")
        return False
    elif calculateHashForBlock(newBlock) != newBlock.hash:
        print("Hash is invalid")
        return False
    return True

def isValidChain(bcToValidate):
    if not isSameBlock(bcToValidate[0], getGenesisBlock()):
        print('Genesis Block Incorrect')
        return False

    tempBlocks = [bcToValidate[0]]
    for i in range(1, len(bcToValidate)):
        if isValidNewBlock(bcToValidate[i], tempBlocks[i-1]):
            tempBlocks.append(bcToValidate[i])
        else:
            return False
    return True
