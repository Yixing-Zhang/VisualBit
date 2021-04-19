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

import json


class Config(object):
    """
    This class manages configurations.
    This is a singleton class.
    """

    __species = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self):
        if self.__first_init:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.configs = json.load(f)
                f.close()
            self.__class__.__first_init = False

    def update(self):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.configs, f, ensure_ascii=False)
            f.close()

    def over_write(self, new_configs):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(new_configs, f, ensure_ascii=False)
            f.close()
        self.configs = new_configs

    def __str__(self):
        return "Configurations: %s" % self.configs
