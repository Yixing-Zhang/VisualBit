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

from bitcoin_parser.blockchain import Blockchain
import config
from utils import dbManager


class DataParser(object):
    """
    This class models the bitcoin data bitcoin_parser.
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
            self.configs = config.Config().configs
            self.__class__.__first_init = False

    def parseBlockFiles(self):
        print("Block files parsing & database constructing started")
        print("This will take a long time. Please do not shut down the power.")
        print('#' * 30)
        print()
        manager = dbManager.DBManager()
        blockchain = Blockchain(self.configs['dp']['block_path'])
        blk_list = blockchain.get_unordered_blocks()

        # load block parsed logs
        try:
            fr = open(self.configs['dp']['log_path'], 'r')
            blk_logs = fr.readline()
            fr.close()
        except Exception:
            print('Parsed logs not found')
            blk_logs = '0' * 2500
            fw = open(self.configs['dp']['log_path'], 'w')
            fw.write(blk_logs)
            fw.close()
        logs_length = len(blk_logs)

        # parsing blocks
        for blks in blk_list:
            # check blk files whether parsed before
            blk_file = blks[0].blk_file
            print('.' * 30)
            print("blk file:", blk_file)
            blk_idx = int(blk_file[3:8])
            if logs_length > blk_idx:
                if blk_logs[blk_idx] == '1':
                    print(blk_file + " parsed before")
                    print(blk_file + " finished")
                    continue
            else:
                for i in range(0, blk_idx - logs_length + 1):
                    blk_logs += '0'
                fw = open(self.configs['dp']['log_path'], 'w')
                fw.write(blk_logs)

            for blk in blks:
                # print("Parsing block:")
                # print(" hash:", blk.hash)
                # print(" tx_no:", blk.n_transactions)
                tx_list = blk.transactions

                # parsing transactions
                tx_insert_query = "INSERT INTO transaction (hash, is_coinbase, outputs_number) VALUES (%s, %s, %s)"
                tx_args = []
                for tx in tx_list:
                    tx_args.append((tx.txid, tx.is_coinbase(), tx.n_outputs))
                    # last_id_query = "SELECT LAST_INSERT_ID()"
                    # tx_id = manager.execute_query(last_id_query)[0][0]
                    # print("last_id:", tx_id)
                    # print(transaction_insert_query)
                    # print("tx_hash:", tx.txid)
                    # print("is_coinbase:", tx.is_coinbase())
                    # print("number_of_outputs:", tx.n_outputs)
                manager.execute_queries(tx_insert_query, tx_args)

                # parsing inputs and outputs
                output_insert_query = "INSERT INTO output (tx_id, pos_index, value, address) VALUES (%s, %s, %s, %s)"
                output_args = []
                input_insert_query = "INSERT INTO input (tx_id, pre_tx_hash, pos_index) VALUES (%s, %s, %s)"
                input_args = []
                for tx in tx_list:
                    tx_id_query = "SELECT tx_id from transaction where hash = '%s'" % tx.txid
                    tx_ids = manager.execute_query(tx_id_query)
                    if not tx_ids:
                        continue
                    tx_id = tx_ids[0][0]
                    if tx.n_outputs > 0:
                        for idx, output in enumerate(tx.outputs):
                            if output.addresses:
                                output_args.append((tx_id, idx, output.value, output.addresses[0].address))
                                # print(output_insert_query)
                                # print("output:", idx, output.value, output.addresses[0].address)
                    if tx.n_inputs > 0:
                        for input in tx.inputs:
                            pos_idx = input.transaction_index
                            if pos_idx != 4294967295:
                                input_args.append((tx_id, input.transaction_hash, pos_idx))
                                # print(input_insert_query)
                                # print("input:", input.transaction_hash, input.transaction_index)
                if output_args:
                    manager.execute_queries(output_insert_query, output_args)
                if input_args:
                    manager.execute_queries(input_insert_query, input_args)

                config.Config().over_write(self.configs)
                # print("Parsing completed.")
                # print('-' * 30)
            print(blk_file + " finished")
            blk_logs = list(blk_logs)
            blk_logs[blk_idx] = '1'
            blk_logs = "".join(blk_logs)
            fw = open(self.configs['dp']['log_path'], 'w')
            fw.write(blk_logs)
        print("All blk files finished.")
