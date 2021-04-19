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

import struct


def uint1(stream):
    return ord(stream.read(1))


def uint2(stream):
    return struct.unpack('H', stream.read(2))[0]


def uint4(stream):
    return struct.unpack('I', stream.read(4))[0]


def uint8(stream):
    return struct.unpack('Q', stream.read(8))[0]


def hash32(stream):
    return stream.read(32)[::-1]


def varint(stream):
    size = uint1(stream)
    if size < 0xfd:
        return size
    if size == 0xfd:
        return uint2(stream)
    if size == 0xfe:
        return uint4(stream)
    if size == 0xff:
        return uint8(stream)
    return -1


def hashStr(bytebuffer):
    return ''.join(('%x' % a) for a in bytebuffer)
