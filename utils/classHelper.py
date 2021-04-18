from binascii import hexlify, unhexlify
import hashlib
from bitcoin import base58


def bip69_sort(data):
    return list(sorted(data, key=lambda t: (t[0], t[1])))


def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def format_hash(hash_):
    return str(hexlify(hash_[::-1]).decode("utf-8"))


def btc_ripemd160(data):
    h1 = hashlib.sha256(data).digest()
    r160 = hashlib.new("ripemd160")
    r160.update(h1)
    return r160.digest()


def validateAddress(address):
    base58Decoder = base58.decode(address).hex()
    prefixAndHash = base58Decoder[:len(base58Decoder) - 8]
    checksum = base58Decoder[len(base58Decoder) - 8:]
    h = prefixAndHash
    for x in range(1, 3):
        h = hashlib.sha256(unhexlify(h)).hexdigest()
    if checksum == h[:8]:
        return True
    else:
        return False

