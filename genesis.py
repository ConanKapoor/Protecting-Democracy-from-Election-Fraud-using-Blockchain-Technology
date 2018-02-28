################################################################################
# Author - Shivam Kapoor (mailme@shivamkapoor.me)
#
# Implementation for "Protecting Democracy from Election
# Fraud using Blockchain Technology"
#
# Github : https://github.com/ConanKapoor/Protecting-Democracy-from
# -Election-Fraud-using-Blockchain-Technology
################################################################################

""" Importing Essentials """
import hashlib
import random
import time
import csv

"""
A class for all of blocks to abide by. It should have the attributes:

    1) Index – it’s position in the blockchain.
    2) Previous Hash – the hash of the block that came before the current block.
    3) Timestamp – the time the block was created.
    4) Data – the information (e.g. transactions) that the block carries.
    5) Hash – the hash of the block itself.
"""
class Block:
    def __init__(self, index, previousHash, timestamp, data, proof, currentHash):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.currentHash = currentHash
        self.proof = proof

"""
    Genesis block is the first block in any blockchain.
    The only requirements are that the genesis has index of 0 and the timestamp is
    less than the current time.
"""
def getGenesisBlock():
    return Block(0, '0', '1496518102.896031', "My very first block :)", 0, '02d779570304667b4c28ba1dbfd4428844a7cab89023205c66858a40937557f8')

""" Function to calculate SHA256 hash. """
def calculateHash(index, previousHash, timestamp, data, proof):
    value = str(index) + str(previousHash) + str(timestamp) + str(data) + str(proof)
    sha = hashlib.sha256(value.encode('utf-8'))
    return str(sha.hexdigest())

""" Function to calculate SHA256 hash. """
def calculateHashForBlock(block):
    return calculateHash(block.index, block.previousHash, block.timestamp, block.data, block.proof)

"""
A function to add blocks to the blockchain.
This section will incorporate a function that can retrieve our latest block.
"""
def getLatestBlock(blockchain):
    return blockchain[len(blockchain)-1]

def generateNextBlock(blockchain, blockData, timestamp, proof):
    previousBlock = getLatestBlock(blockchain)
    nextIndex = int(previousBlock.index) + 1
    nextTimestamp = timestamp
    nextHash = calculateHash(nextIndex, previousBlock.currentHash, nextTimestamp, proof, blockData)
    return Block(nextIndex, previousBlock.currentHash, nextTimestamp, blockData, proof, nextHash)

"""
    This section involves making sure these blocks are legitimate and checking the
    entire chain.

    The "isValidNewBlock" function determines if the block is valid based on hashes
    and indicesmatching up.

    Using the two functions above, we can check the validity of an entire chain by
    using the "isValidChain" function iterating over the entire list in a for loop:
"""
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

def writeBlockchain(blockchain):
    blockchainList = []
    for block in blockchain:
        blockList = [block.index, block.previousHash, str(block.timestamp), block.data, block.proof, block.currentHash]
        blockchainList.append(blockList)

    with open("blockchain.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(blockchainList)

    print('Blockchain written to blockchain.csv.')

def readBlockchain(blockchainFilePath):
    importedBlockchain = []
    try:
        with open(blockchainFilePath, 'r') as file:
            blockReader = csv.reader(file)
            for line in blockReader:
                block = Block(line[0], line[1], line[2], line[3], line[4], line[5])
                importedBlockchain.append(block)
        print("Pulling blockchain from csv...")
        return importedBlockchain
    except:
        print('No blockchain located. Generating new genesis block...')
        return [getGenesisBlock()]

"""
    The below mining section leverages a simple generator that creates 5 mock
    transactions – mimicking the process of taking transactions from a mempool.

    These randomly generated transactions act as the blockData.

    "getTxData" function simply creates a long string of 5 transactions with the
    format: “User <random number> sent <random number> tokens to user
    <random number>.” all concatenated together.
"""
def getTxData():
    txData = ''
    for _ in range(5):
        txTo, txFrom, amount = random.randrange(0, 1000), random.randrange(0, 1000), random.randrange(0, 100)
        transaction = 'User ' + str(txFrom) + " sent " + str(amount) + ' tokens to user ' + str(txTo) + ". "
        txData += transaction
    return txData

"""
    "mineNewBlock" Function takes in a difficultly level and a file path for the
    blockchain .csv, which both are set to defaults.

    Difficulty is the number of leading 0’s in the hash.
    (e.g. a difficulty of 5 would have a hash like 00000b4JA7…).

    Essentially the mining algorithm starts with an attempt to get this hash
    with proof = 0. If the concatenation of this proof at the end of the block
    creates a hash with the desired amount of 0’s, this is appended to the end
    of the blockchain.
"""
def mineNewBlock(difficulty = 5, blockchainPath = 'blockchain.csv'):
    blockchain = readBlockchain(blockchainPath)
    txData = getTxData()
    timestamp = time.time()
    proof = 0
    newBlockFound = False
    print('Mining a block...')
    while not newBlockFound:
        newBlockAttempt = generateNextBlock(blockchain, txData, timestamp, proof)
        if newBlockAttempt.currentHash[0:difficulty] == '0'*difficulty:
            stopTime = time.time()
            timer = stopTime - timestamp
            print('New block found with proof', proof, 'in', round(timer, 2), 'seconds.')

            newBlockFound = True
        else:
            proof += 1
    blockchain.append(newBlockAttempt)
    writeBlockchain(blockchain)


def mine(blocksToMine = 5):
    for _ in range(blocksToMine):
        mineNewBlock()
