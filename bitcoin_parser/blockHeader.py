# This file is modified from https://github.com/alecalve/python-bitcoin-blockchain-parser


from datetime import datetime
from bitcoin.core import CBlockHeader
from utils.classHelper import format_hash
from utils.streamer import decode_uint32


class BlockHeader(object):
    """
    Represents a block header
    """

    def __init__(self, raw_hex):
        self._version = None
        self._previous_block_hash = None
        self._merkle_root = None
        self._timestamp = None
        self._bits = None
        self._nonce = None
        self._difficulty = None

        self.hex = raw_hex[:80]

    def __repr__(self):
        return "BlockHeader(previous_block_hash=%s)" % self.previous_block_hash

    @classmethod
    def from_hex(cls, raw_hex):
        """
        Builds a BlockHeader object from its bytes representation
        """
        return cls(raw_hex)

    @property
    def version(self):
        """
        Return the block's version
        """
        if self._version is None:
            self._version = decode_uint32(self.hex[:4])
        return self._version

    @property
    def previous_block_hash(self):
        """
        Return the hash of the previous block
        """
        if self._previous_block_hash is None:
            self._previous_block_hash = format_hash(self.hex[4:36])
        return self._previous_block_hash

    @property
    def merkle_root(self):
        """
        Returns the block's merkle root
        """
        if self._merkle_root is None:
            self._merkle_root = format_hash(self.hex[36:68])
        return self._merkle_root

    @property
    def timestamp(self):
        """
        Returns the timestamp of the block as a UTC datetime object
        """
        if self._timestamp is None:
            self._timestamp = datetime.utcfromtimestamp(
                decode_uint32(self.hex[68:72])
            )
        return self._timestamp

    @property
    def bits(self):
        """
        Returns the bits (difficulty target) of the block
        """
        if self._bits is None:
            self._bits = decode_uint32(self.hex[72:76])
        return self._bits

    @property
    def nonce(self):
        """
        Returns the block's nonce
        """
        if self._nonce is None:
            self._nonce = decode_uint32(self.hex[76:80])
        return self._nonce

    @property
    def difficulty(self):
        """
        Returns the block's difficulty target as a float
        """
        if self._difficulty is None:
            self._difficulty = CBlockHeader.calc_difficulty(self.bits)

        return self._difficulty
