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

from utils import dbManager
import config

# connect to database server
manager = dbManager.DBManager()
manager.create_server_connection()

# connect to database
manager.create_db_connection()
if manager.db_connection is None:
    manager.create_database()
    manager.create_db_connection()

# check and drop tables
manager.drop_db_tables()
config.Config().configs['dp']['parse_index'] = -1
config.Config().update()
