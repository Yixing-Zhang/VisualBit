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


def decode_uint32(data):
    assert (len(data) == 4)
    return struct.unpack("<I", data)[0]


def decode_uint64(data):
    assert (len(data) == 8)
    return struct.unpack("<Q", data)[0]


def decode_varint(data):
    assert (len(data) > 0)
    size = int(data[0])
    assert (size <= 255)

    if size < 253:
        return size, 1

    if size == 253:
        format_ = '<H'
    elif size == 254:
        format_ = '<I'
    elif size == 255:
        format_ = '<Q'
    else:
        # Should never be reached
        assert 0, "unknown format_ for size : %s" % size

    size = struct.calcsize(format_)
    return struct.unpack(format_, data[1:size + 1])[0], size + 1
