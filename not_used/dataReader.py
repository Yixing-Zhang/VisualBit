import config
import os
import datetime
import hashlib


def reverse(input):
    L = len(input)
    if (L % 2) != 0:
        return None
    else:
        Res = ''
        L = L // 2
        for i in range(L):
            T = input[i * 2] + input[i * 2 + 1]
            Res = T + Res
            T = ''
        return Res


def sha256d(x):
    return hashlib.sha256(hashlib.sha256(x).digest()).digest()


def hash_pair(x, y):
    return sha256d(x[::-1] + y[::-1])[::-1]


def merkle_root(lst):
    if len(lst) == 1:
        return lst[0]
    if len(lst) % 2 == 1:
        lst.append(lst[-1])
    return merkle_root([hash_pair(x, y) for x, y in zip(*[iter(lst)] * 2)])


def read_bytes(file, n, byte_order='L'):
    data = file.read(n)
    if byte_order == 'L':
        data = data[::-1]
    data = data.hex().upper()
    return data


def read_varint(file):
    b = file.read(1)
    bInt = int(b.hex(), 16)
    c = 0
    data = ''
    if bInt < 253:
        c = 1
        data = b.hex().upper()
    if bInt == 253:
        c = 3
    if bInt == 254:
        c = 5
    if bInt == 255:
        c = 9
    for i in range(1, c):
        b = file.read(1)
        b = b.hex().upper()
        data = b + data
    return data


def read_file_list(fList, block_path, save_path, debug=False):
    for i in fList:
        nameSrc = i
        nameRes = nameSrc.replace('.dat', '.txt')
        resList = []
        a = 0
        t = block_path + "\\" + nameSrc
        resList.append('[' + str(datetime.datetime.now()) + ']' + 'Read ' + t)
        print('[' + str(datetime.datetime.now()) + '] ' + 'Read ' + t)
        try:
            f = open(t, 'rb')
        except Exception:
            print('Block file' + nameSrc + 'not found')
        tmpHex = ''
        fSize = os.path.getsize(t)
        while f.tell() != fSize:
            tmpHex = read_bytes(f, 4)
            resList.append('#' * 30 + 'Block' + '#' * 30)
            resList.append('=' * 10 + 'Block Header' + '=' * 10)
            resList.append('Magic number =\t' + tmpHex)
            if debug:
                print('#' * 30 + 'Block' + '#' * 30)
                print('=' * 10 + 'Block Header' + '=' * 10)
                print('Magic number =\t' + tmpHex)
            tmpHex = read_bytes(f, 4)
            resList.append('Block size =\t' + tmpHex)
            if debug:
                print('Block size =\t' + tmpHex)
            tmpPos3 = f.tell()
            tmpHex = read_bytes(f, 80, 'B')
            tmpHex = bytes.fromhex(tmpHex)
            tmpHex = hashlib.new('sha256', tmpHex).digest()
            tmpHex = hashlib.new('sha256', tmpHex).digest()
            tmpHex = tmpHex[::-1]
            tmpHex = tmpHex.hex().upper()
            resList.append('SHA256 hash of the current block hash =\t' + tmpHex)
            if debug:
                print('SHA256 hash of the current block hash =\t' + tmpHex)
            f.seek(tmpPos3, 0)
            tmpHex = read_bytes(f, 4)
            resList.append('Version number =\t' + tmpHex)
            if debug:
                print('Version number = ' + tmpHex)
            tmpHex = read_bytes(f, 32)
            resList.append('SHA256 hash of the previous block hash =\t' + tmpHex)
            if debug:
                print('SHA256 hash of the previous block hash =\t' + tmpHex)
            tmpHex = read_bytes(f, 32)
            resList.append('MerkleRoot hash =\t' + tmpHex)
            if debug:
                print('MerkleRoot hash =\t' + tmpHex)
            MerkleRoot = tmpHex
            tmpHex = read_bytes(f, 4)
            resList.append('Time stamp =\t' + tmpHex)
            if debug:
                print('Time stamp =\t' + tmpHex)
            tmpHex = read_bytes(f, 4)
            resList.append('Difficulty =\t' + tmpHex)
            if debug:
                print('Difficulty =\t' + tmpHex)
            tmpHex = read_bytes(f, 4)
            resList.append('Random number =\t' + tmpHex)
            if debug:
                print('Random number =\t' + tmpHex)
            tmpHex = read_varint(f)
            txCount = int(tmpHex, 16)
            resList.append('')
            resList.append('Transactions count =\t' + str(txCount))
            if debug:
                print('')
                print('Transactions count =\t' + str(txCount))
            resList.append('')
            if debug:
                print('')
            tmpHex = ''
            RawTX = ''
            tx_hashes = []
            for k in range(txCount):
                tmpHex = read_bytes(f, 4)
                resList.append('=' * 10 + 'Transaction' + '=' * 10)
                resList.append('TX version number =\t' + tmpHex)
                if debug:
                    print('=' * 10 + 'Transaction' + '=' * 10)
                    print('TX version number =\t' + tmpHex)
                RawTX = reverse(tmpHex)
                tmpHex = ''
                Witness = False
                b = f.read(1)
                tmpB = b.hex().upper()
                bInt = int(b.hex(), 16)
                if bInt == 0:
                    tmpB = ''
                    f.seek(1, 1)
                    c = 0
                    c = f.read(1)
                    bInt = int(c.hex(), 16)
                    tmpB = c.hex().upper()
                    Witness = True
                c = 0
                if bInt < 253:
                    c = 1
                    tmpHex = hex(bInt)[2:].upper().zfill(2)
                    tmpB = ''
                if bInt == 253:
                    c = 3
                if bInt == 254:
                    c = 5
                if bInt == 255:
                    c = 9
                for j in range(1, c):
                    b = f.read(1)
                    b = b.hex().upper()
                    tmpHex = b + tmpHex
                inCount = int(tmpHex, 16)
                resList.append('Inputs count =\t' + tmpHex)
                if debug:
                    print('Inputs count =\t' + tmpHex)
                tmpHex = tmpHex + tmpB
                RawTX = RawTX + reverse(tmpHex)
                for m in range(inCount):
                    resList.append('-' * 10 + 'Input' + '-' * 10)
                    tmpHex = read_bytes(f, 32)
                    resList.append('TX from hash =\t' + tmpHex)
                    if debug:
                        print('-' * 10 + 'Input' + '-' * 10)
                        print('TX from hash =\t' + tmpHex)
                    RawTX = RawTX + reverse(tmpHex)
                    tmpHex = read_bytes(f, 4)
                    resList.append('Tx Out Index =\t' + tmpHex)
                    if debug:
                        print('Tx Out Index =\t' + tmpHex)
                    RawTX = RawTX + reverse(tmpHex)
                    tmpHex = ''
                    b = f.read(1)
                    tmpB = b.hex().upper()
                    bInt = int(b.hex(), 16)
                    c = 0
                    if bInt < 253:
                        c = 1
                        tmpHex = hex(bInt)[2:].upper().zfill(2)
                        tmpB = ''
                    if bInt == 253:
                        c = 3
                    if bInt == 254:
                        c = 5
                    if bInt == 255:
                        c = 9
                    for j in range(1, c):
                        b = f.read(1)
                        b = b.hex().upper()
                        tmpHex = b + tmpHex
                    scriptLength = int(tmpHex, 16)
                    tmpHex = tmpHex + tmpB
                    RawTX = RawTX + reverse(tmpHex)
                    tmpHex = read_bytes(f, scriptLength, 'B')
                    resList.append('Input script =\t' + tmpHex)
                    if debug:
                        print('Input script =\t' + tmpHex)
                    RawTX = RawTX + tmpHex
                    tmpHex = read_bytes(f, 4, 'B')
                    resList.append('Sequence number =\t' + tmpHex)
                    if debug:
                        print('Sequence number =\t' + tmpHex)
                    RawTX = RawTX + tmpHex
                    tmpHex = ''
                b = f.read(1)
                tmpB = b.hex().upper()
                bInt = int(b.hex(), 16)
                c = 0
                if bInt < 253:
                    c = 1
                    tmpHex = hex(bInt)[2:].upper().zfill(2)
                    tmpB = ''
                if bInt == 253:
                    c = 3
                if bInt == 254:
                    c = 5
                if bInt == 255:
                    c = 9
                for j in range(1, c):
                    b = f.read(1)
                    b = b.hex().upper()
                    tmpHex = b + tmpHex
                outputCount = int(tmpHex, 16)
                tmpHex = tmpHex + tmpB
                resList.append('')
                resList.append('Outputs count =\t' + str(outputCount))
                resList.append('-' * 10 + 'Output' + '-' * 10)
                if debug:
                    print('')
                    print('Outputs count =\t' + str(outputCount))
                    print('-' * 10 + 'Output' + '-' * 10)
                RawTX = RawTX + reverse(tmpHex)
                for m in range(outputCount):
                    tmpHex = read_bytes(f, 8)
                    Value = tmpHex
                    RawTX = RawTX + reverse(tmpHex)
                    tmpHex = ''
                    b = f.read(1)
                    tmpB = b.hex().upper()
                    bInt = int(b.hex(), 16)
                    c = 0
                    if bInt < 253:
                        c = 1
                        tmpHex = hex(bInt)[2:].upper().zfill(2)
                        tmpB = ''
                    if bInt == 253:
                        c = 3
                    if bInt == 254:
                        c = 5
                    if bInt == 255:
                        c = 9
                    for j in range(1, c):
                        b = f.read(1)
                        b = b.hex().upper()
                        tmpHex = b + tmpHex
                    scriptLength = int(tmpHex, 16)
                    tmpHex = tmpHex + tmpB
                    RawTX = RawTX + reverse(tmpHex)
                    tmpHex = read_bytes(f, scriptLength, 'B')
                    resList.append('Value =\t' + Value)
                    if debug:
                        print('Value =\t' + Value)
                    resList.append('Output script =\t' + tmpHex)
                    if debug:
                        print('Output script =\t' + tmpHex)
                    RawTX = RawTX + tmpHex
                    tmpHex = ''
                resList.append('')
                if debug:
                    print('')
                if Witness:
                    for m in range(inCount):
                        tmpHex = read_varint(f)
                        WitnessLength = int(tmpHex, 16)
                        for j in range(WitnessLength):
                            tmpHex = read_varint(f)
                            WitnessItemLength = int(tmpHex, 16)
                            tmpHex = read_bytes(f, WitnessItemLength)
                            resList.append(
                                'Witness ' + str(m) + ' ' + str(j) + ' ' + str(WitnessItemLength) + ' ' + tmpHex)
                            if debug:
                                print(
                                    'Witness ' + str(m) + ' ' + str(j) + ' ' + str(WitnessItemLength) + ' ' + tmpHex)
                            tmpHex = ''
                Witness = False
                tmpHex = read_bytes(f, 4)
                resList.append('Lock time =\t' + tmpHex)
                if debug:
                    print('Lock time =\t' + tmpHex)
                RawTX = RawTX + reverse(tmpHex)
                tmpHex = RawTX
                tmpHex = bytes.fromhex(tmpHex)
                tmpHex = hashlib.new('sha256', tmpHex).digest()
                tmpHex = hashlib.new('sha256', tmpHex).digest()
                tmpHex = tmpHex[::-1]
                tmpHex = tmpHex.hex().upper()
                resList.append('TX hash =\t' + tmpHex)
                if debug:
                    print('TX hash =\t' + tmpHex)
                tx_hashes.append(tmpHex)
                resList.append('')
                if debug:
                    print('')
                tmpHex = ''
                RawTX = ''
            a += 1
            tx_hashes = [bytes.fromhex(h) for h in tx_hashes]
            tmpHex = merkle_root(tx_hashes).hex().upper()
            if tmpHex != MerkleRoot:
                print('Merkle roots does not match! >', MerkleRoot, tmpHex)
        f.close()

        print('[' + str(datetime.datetime.now()) + '] ' + "Save " + save_path + "\\" + nameRes)
        f = open(save_path + "\\" + nameRes, 'w')
        for j in resList:
            f.write(j + '\n')
        f.close()


def read_data(block_path, save_path, start=-1, end=-1, debug=False):
    if start == -1:
        fList = os.listdir(block_path)
        fList = [x for x in fList if (x.endswith('.dat') and x.startswith('blk'))]
        fList.sort()

        read_file_list(fList, block_path, save_path, debug)
    else:
        fList = ["blk" + str(i).zfill(5) + '.dat' for i in range(start, end + 1)]

        read_file_list(fList, block_path, save_path, debug)


'''
print("Analyzing block 1...")
print(" Hash:                     "
      "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb604800000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048")
print(" Blcok timestamp:          2009-01-09 10:54")
print(" Number of transactions:   1")
print()
print(" Transactions:")
print("""
    Hash: 0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098
        #input
        COINBASE (Newly Generated Coins)
        
        #output
        12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX 50
""")
print("Analyzing finished")
print()
print("Saving to database...")
print("Saving successfully")
'''

configs = config.configs
block_path = configs['dp']['block_path']
save_path = configs['dp']['save_path']
read_data(block_path, save_path, -1, -1, False)
