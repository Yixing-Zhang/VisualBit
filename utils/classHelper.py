# VisualBit - A tool to facilitate the analyses of Bitcoin transactions
# Copyright (C) <2021>  <Zhang Yixing>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Email: u3544946@connect.hku.hk

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

