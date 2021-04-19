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

import mysql.connector
import config


class DBManager(object):
    """
    This class manages the interactions with MySQL database.
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
            self.server_connection = None
            self.db_connection = None
            self.__class__.__first_init = False

    def create_server_connection(self):
        """
        Try to connect to the MySQL server in the config file.
        """
        try:
            self.server_connection = mysql.connector.connect(
                host=self.configs['db']['host'],
                user=self.configs['db']['user'],
                passwd=self.configs['db']['password']
            )
            print("MySQL Server " + self.configs['db']['host'] + " connection successful")
        except Exception as err:
            print(f"Error: '{err}'")

    def create_database(self):
        """
        Try to create a database with the name stated in the config file.
        """
        print("Creating database...")
        cursor = self.server_connection.cursor()
        try:
            creat_database_query = "CREATE DATABASE " + self.configs['db']['dbName']
            cursor.execute(creat_database_query)
            cursor.close()
            print("Database " + self.configs['db']['dbName'] + " created successfully")
        except Exception as err:
            cursor.close()
            print(f"Error: '{err}'")

    def create_db_connection(self):
        """
        Try to connect to the database with the name stated in the config file.
        """
        try:
            self.db_connection = mysql.connector.connect(
                host=self.configs['db']['host'],
                user=self.configs['db']['user'],
                passwd=self.configs['db']['password'],
                database=self.configs['db']['dbName']
            )
            print("MySQL Database " + self.configs['db']['dbName'] + " connection successful")
        except Exception as err:
            print(f"Error: '{err}'")

    def execute_query(self, query):
        """
        Try to execute an arbitrary query in the database.

        :param query: the query to be executed
        """
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            self.db_connection.commit()
            cursor.close()
            # print("Query successful")
            return result
        except Exception as err:
            print(f"Error: '{err}'")
            cursor.close()
            return None

    def execute_queries(self, queries, args):
        """
        Try to execute a list of queries in the database.

        :param queries: the queries to be executed
        """
        cursor = self.db_connection.cursor()
        try:
            cursor.executemany(queries, args)
            self.db_connection.commit()
            cursor.close()
            # print("Query successful")
        except Exception as err:
            print(f"Error: '{err}'")
            cursor.close()

    def create_db_tables(self):
        """
        Try to create the 4 tables in the database if they don't exist.
        """
        # transaction table
        tableQuery = "SHOW TABLES LIKE 'transaction'"
        result = self.execute_query(tableQuery)
        if result:
            # there is a table named "transaction"
            print("Table transaction exists")
        else:
            # there are no tables named "transaction"
            print("Table transaction doesn't exist")
            try:
                create_transaction_table_query = """
                CREATE TABLE transaction(
                    tx_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    hash VARCHAR(64) UNIQUE NOT NULL,
                    is_coinbase BOOL NOT NULL,
                    outputs_number INT NOT NULL
                )
                """
                self.execute_query(create_transaction_table_query)
                print("Table transaction created")
            except Exception as err:
                print(f"Error: '{err}'")

        # output table
        tableQuery = "SHOW TABLES LIKE 'output'"
        result = self.execute_query(tableQuery)
        if result:
            # there is a table named "output"
            print("Table output exists")
        else:
            # there are no tables named "output"
            print("Table output doesn't exist")
            try:
                create_output_table_query = """
                CREATE TABLE output(
                    output_id INT AUTO_INCREMENT PRIMARY KEY,
                    tx_id BIGINT NOT NULL,
                    pos_index INT NOT NULL,
                    value BIGINT NOT NULL,
                    address VARCHAR(35) NOT NULL,
                    FOREIGN KEY (tx_id) REFERENCES transaction(tx_id),
                    UNIQUE tx (tx_id, pos_index)
                )
                """
                self.execute_query(create_output_table_query)
                print("Table output created")
            except Exception as err:
                print(f"Error: '{err}'")

        # input table
        tableQuery = "SHOW TABLES LIKE 'input'"
        result = self.execute_query(tableQuery)
        if result:
            # there is a table named "input"
            print("Table input exists")
        else:
            # there are no tables named "input"
            print("Table input doesn't exist")
            try:
                create_input_table_query = """
                CREATE TABLE input(
                    input_id INT AUTO_INCREMENT PRIMARY KEY,
                    tx_id BIGINT NOT NULL,
                    output_id INT UNIQUE,
                    pre_tx_hash CHAR(64) NOT NULL,
                    pos_index INT NOT NULL,
                    FOREIGN KEY (tx_id) REFERENCES transaction(tx_id),
                    FOREIGN KEY (output_id) REFERENCES output(output_id),
                    UNIQUE tx (pre_tx_hash, pos_index)
                )
                """
                self.execute_query(create_input_table_query)
                print("Table input created")
            except Exception as err:
                print(f"Error: '{err}'")

        # cluster table
        tableQuery = "SHOW TABLES LIKE 'cluster'"
        result = self.execute_query(tableQuery)
        if result:
            # there is a table named "cluster"
            print("Table cluster exists")
        else:
            # there are no tables named "input"
            print("Table cluster doesn't exist")
            try:
                create_cluster_table_query = """
                CREATE TABLE cluster(
                    cluster_id INT AUTO_INCREMENT PRIMARY KEY,
                    address VARCHAR(35) UNIQUE NOT NULL,
                    tag VARCHAR(30)
                )
                """
                self.execute_query(create_cluster_table_query)
                print("Table cluster created")
            except Exception as err:
                print(f"Error: '{err}'")

    def drop_db_tables(self):
        """
            Try to drop the 3 tables in the database if they exist.
        """
        # input table
        tableQuery = "SHOW TABLES LIKE 'input'"
        result = self.execute_query(tableQuery)
        if result:
            # there is a table named "input"
            print("Table input exists")
            try:
                drop_input_table_query = """
                        DROP TABLE input
                        """
                self.execute_query(drop_input_table_query)
                print("Table input dropped")
            except Exception as err:
                print(f"Error: '{err}'")
        else:
            # there are no tables named "input"
            print("Table input doesn't exist")

        # output table
        tableQuery = "SHOW TABLES LIKE 'output'"
        result = self.execute_query(tableQuery)
        if result:
            # there is a table named "output"
            print("Table output exists")
            try:
                drop_output_table_query = """
                DROP TABLE output
                """
                self.execute_query(drop_output_table_query)
                print("Table output dropped")
            except Exception as err:
                print(f"Error: '{err}'")
        else:
            # there are no tables named "output"
            print("Table output doesn't exist")

        # transaction table
        tableQuery = "SHOW TABLES LIKE 'transaction'"
        result = self.execute_query(tableQuery)
        if result:
            # there is a table named "transaction"
            print("Table transaction exists")
            try:
                drop_transaction_table_query = """
                    DROP TABLE transaction
                    """
                self.execute_query(drop_transaction_table_query)
                print("Table transaction dropped")
            except Exception as err:
                print(f"Error: '{err}'")
        else:
            # there are no tables named "transaction"
            print("Table transaction doesn't exist")

        # cluster table
        tableQuery = "SHOW TABLES LIKE 'cluster'"
        result = self.execute_query(tableQuery)
        if result:
            # there is a table named "cluster"
            print("Table cluster exists")
            try:
                drop_cluster_table_query = """
                        DROP TABLE cluster
                        """
                self.execute_query(drop_cluster_table_query)
                print("Table cluster dropped")
            except Exception as err:
                print(f"Error: '{err}'")
        else:
            # there are no tables named "cluster"
            print("Table cluster doesn't exist")
