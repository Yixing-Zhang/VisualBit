import os
import datetime
import config
from streamer import *


class Block:
    def __init__(self, blockchain):
        self.magicNum = uint4(blockchain)
        self.blockSize = uint4(blockchain)
        self.blockHeader = BlockHeader(blockchain)
        self.txCount = varint(blockchain)
        self.Txs = []
        for i in range(0, self.txCount):
            tx = Tx(blockchain)
            self.Txs.append(tx)

    def toStringDB(self, save_path):
        output = open(save_path, 'a')
        output.write("\n")
        output.write("=" * 30 + " Block " + "=" * 30)
        output.write("\n")
        output.write("Magic No:\t %8x \n" % self.magicNum)
        output.write("Block Size:\t %d \n" % self.blockSize)
        output.write("\n")
        self.blockHeader.toStringDB(save_path)
        output.write("------ Tx Count: %d\n" % self.txCount)
        for t in self.Txs:
            t.toStringDB(save_path)


class BlockHeader:
    def __init__(self, blockchain):
        self.version = uint4(blockchain)
        self.previousHash = hash32(blockchain)
        self.merkleHash = hash32(blockchain)
        self.time = uint4(blockchain)
        self.bits = uint4(blockchain)
        self.nonce = uint4(blockchain)

    def toStringDB(self, save_path):
        output = open(save_path, 'a')
        output.write("=" * 10 + " Block Header " + "=" * 10)
        output.write("\n")
        output.write("Version:\t %d \n" % self.version)
        output.write("Previous Hash:\t\t %s \n" % hashStr(self.previousHash))
        output.write("Merkle Root Hash:\t\t %s \n" % hashStr(self.merkleHash))
        output.write("Time:\t %s \n")
        output.write("Bits:\t %8x \n" % self.bits)
        output.write("Nonce:\t %s \n" % self.nonce)


class Tx:
    def __init__(self, blockchain):
        self.version = uint4(blockchain)
        self.inCount = varint(blockchain)
        self.inputs = []
        for i in range(0, self.inCount):
            input = TxInput(blockchain)
            self.inputs.append(input)
        self.outCount = varint(blockchain)
        self.outputs = []
        if self.outCount > 0:
            for i in range(0, self.outCount):
                output = TxOutput(blockchain)
                self.outputs.append(output)
        self.lockTime = uint4(blockchain)
        self.tx_hash = None

    def toStringDB(self, save_path):
        output = open(save_path, 'a')
        output.write("\n")
        output.write("=" * 10 + "Transaction" + "=" * 10)
        output.write("\n")
        output.write("Tx Version:\t %d \n" % self.version)
        output.write("Inputs:\t\t %d \n" % self.inCount)
        for i in self.inputs:
            i.toStringDB(save_path)
        output.write("Outputs:\t\t %d \n" % self.outCount)
        for o in self.outputs:
            o.toStringDB(save_path)
        output.write("Lock Time:\t %d \n" % self.lockTime)
        # transaction_query = "insert into transaction values (" + tx_hash + ", " + block_hash + ", " + is_coinbase +")"
        # self.dbManager.execute_query(transaction_query)


class TxInput:
    def __init__(self, blockchain):
        self.previousHash = hash32(blockchain)
        self.txOutId = uint4(blockchain)
        self.scriptLen = varint(blockchain)
        self.scriptSig = blockchain.read(self.scriptLen)
        self.seqNo = uint4(blockchain)

    def toStringDB(self, save_path):
        output = open(save_path, 'a')
        output.write("\n")
        output.write("-" * 10 + "Inputs" + "-" * 10)
        output.write("\n")
        output.write("Previous Hash:\t\t &d \n" % self.previousHash)
        output.write("Tx Out Index:\t\t %d \n" % self.txOutId)
        output.write("Script Length:\t %d \n" % self.scriptLen)
        output.write("Script Signature:\t %s \n" % hashStr(self.scriptSig))
        output.write("Sequence No:\t\t %s \n" % self.seqNo)


class TxOutput:
    def __init__(self, blockchain):
        self.value = uint8(blockchain)
        self.scriptLen = varint(blockchain)
        self.pubKey = blockchain.read(self.scriptLen)

    def toStringDB(self, save_path):
        output = open(save_path, 'a')
        output.write("\n")
        output.write("-" * 10 + "Outputs" + "-" * 10)
        output.write("\n")
        output.write("Value:\t\t %d \n" % self.value)
        output.write("Script Length:\t %d \n" % self.scriptLen)
        output.write("Public Key:\t\t %s \n" % hashStr(self.pubKey))


def read_file_list(fList, block_path, save_path, debug):
    for i in fList:
        nameSrc = i
        nameRes = nameSrc.replace('.dat', '.txt')
        t = block_path + "\\" + nameSrc
        if debug:
            print('[' + str(datetime.datetime.now()) + '] ' + 'Read ' + t)
        try:
            f = open(t, 'rb')
        except Exception:
            if debug:
                print('Block file' + nameSrc + 'not found')
        fSize = os.path.getsize(t)
        while f.tell() != fSize:
            block = Block(f)
            block.toStringDB(save_path + "\\" + nameRes)
        if debug:
            print('[' + str(datetime.datetime.now()) + '] ' + 'Finish ' + t)


def read_data(block_path, save_path, start=-1, end=-1, debug=False):
    if start == -1:
        fList = os.listdir(block_path)
        fList = [x for x in fList if (x.endswith('.dat') and x.startswith('blk'))]
        fList.sort()

        read_file_list(fList, block_path, save_path, debug)
    else:
        fList = ["blk" + str(i).zfill(5) + '.dat' for i in range(start, end + 1)]

        read_file_list(fList, block_path, save_path, debug)


configs = config.configs
block_path = configs['dp']['block_path']
save_path = configs['dp']['save_path']
read_data(block_path, save_path, 100, 100, True)
