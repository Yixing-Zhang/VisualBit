from utils import dbManager
import random
import time


class Cluster(object):
    """
    This class models the bitcoin address cluster.
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
            self.manager = dbManager.DBManager()
            self.__class__.__first_init = False

    def updateCluster(self, addresses):
        if addresses:
            print('#' * 30)
            print("Updating cluster......")
            tag = str(int(random.random() * 100000)) + str(int(time.time()))
            print("New tag:", tag)
            tags = []
            for address in addresses:
                tags_query = "SELECT tag FROM cluster WHERE address = '%s'" % address
                temp = self.manager.execute_query(tags_query)
                if temp:
                    tags += temp
            tags = list(set(tags))
            if tags:
                print("Old tags:", tags)
                print("Updating old tags......")
                tags_update_query = "UPDATE cluster SET tag = '" + tag + "' WHERE tag = %s"
                self.manager.execute_queries(tags_update_query, tags)
            print("Inserting new cluster......")
            cluster_replace_query = "INSERT INTO cluster (address, tag) VALUES (%s, '" + tag + "') ON DUPLICATE KEY UPDATE tag = '" + tag + "'"
            self.manager.execute_queries(cluster_replace_query, addresses)
            print("Cluster updated......")

    def CS_cluster(self):
        """
        This is the method for commons spending (CS) clustering.
        """
        CS_tx_query = """
        SELECT tx_id
        FROM input
        GROUP BY tx_id
        HAVING COUNT(*) > 1
        """
        tx_ids = self.manager.execute_query(CS_tx_query)
        if tx_ids:
            for tx_id in tx_ids:
                print('#' * 30)
                print("CS transaction:", tx_id[0])
                CS_address_query = """
                SELECT O.address
                FROM output AS O JOIN (SELECT I.tx_id, T.tx_id AS pre_tx_id, I.pos_index
                                        FROM input AS I JOIN transaction AS T
                                        ON I.pre_tx_hash = T.hash
                                        WHERE I.tx_id = %s) AS IT
                ON O.tx_id = IT.pre_tx_id AND O.pos_index = IT.pos_index
                """ % tx_id[0]
                addresses = self.manager.execute_query(CS_address_query)
                if addresses:
                    print("CS addresses:", addresses)
                    self.updateCluster(addresses)

    def OTC_cluster(self):
        """
        This is the method for one-time change (OTC) clustering.
        """
        OTC_address_query = """
        SELECT O.address
        FROM (SELECT input.tx_id, output.address FROM input JOIN transaction JOIN output ON input.pre_tx_hash = transaction.hash AND output.tx_id = transaction.tx_id AND input.pos_index = output.pos_index) AS I
        JOIN (SELECT tx_id, outputs_number FROM transaction WHERE outputs_number = 1) AS T
        JOIN output AS O
        ON I.tx_id = T.tx_id AND T.tx_id = O.tx_id
        GROUP BY O.address
        """
        output_addresses = self.manager.execute_query(OTC_address_query)
        if output_addresses:
            for output_address in output_addresses:
                print('#' * 30)
                print("One output:", output_address[0])
                OTC_tx_query = """
                SELECT I.address
                FROM (SELECT input.tx_id, output.address FROM input JOIN transaction JOIN output ON input.pre_tx_hash = transaction.hash AND output.tx_id = transaction.tx_id AND input.pos_index = output.pos_index) AS I
                JOIN (SELECT tx_id, outputs_number FROM transaction WHERE outputs_number = 1) AS T
                JOIN output AS O
                ON I.tx_id = T.tx_id AND T.tx_id = O.tx_id
                WHERE O.address = '%s'
                """ % output_address[0]
                input_addresses = self.manager.execute_query(OTC_tx_query)
                if input_addresses:
                    print("Input_addresses:", input_addresses)
                    addresses = input_addresses
                    addresses.append(output_address)
                    self.updateCluster(addresses)

    def cluster(self):
        """
        This the main method for clustering using all the two methods.
        """
        print("Addresses cluster & database constructing started")
        print("This will take a long time. Please do not shut down the power.")
        print('#' * 30)
        print("OTC cluster starting......")
        # self.OTC_cluster()
        print("OTC cluster finished......")
        print('#' * 60)
        print("CS cluster starting......")
        self.CS_cluster()
        print("CS cluster finished......")
