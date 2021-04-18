import config
from utils import dbManager, classHelper
from bitcoin_parser import dataParser
from cluster import cluster
from network_generator import networkGenerator

print("Program initializing......")

# load configurations
print("Loading configurations......")
configs = config.Config().configs

print("Connecting to MySQL database......")
manager = dbManager.DBManager()
# connect to database server
manager.create_server_connection()
# connect to database
manager.create_db_connection()
if manager.db_connection is None:
    manager.create_database()
    manager.create_db_connection()

# check and create tables
print("Checking database tables......")
manager.create_db_tables()

# menu
choice = '-1'
print('#' * 60)
print("Welcome to VisualBit V1.0")


def parseData():
    """
    This method handles bitcoin data parsing.
    """
    print('#' * 60)
    bitParser = dataParser.DataParser()
    bitParser.parseBlockFiles()


def deleteData():
    """
    This method handles database deleting.
    """
    print('#' * 60)
    print("Deleting databases")
    dbManager.DBManager().drop_db_tables()
    config.Config().configs['dp']['parse_index'] = -1
    config.Config().update()


def clusterAddress():
    """
    This method handles addresses clustering.
    """
    print('#' * 60)
    bitCluster = cluster.Cluster()
    bitCluster.cluster()


def generateNetworkLocal(address, layer):
    """
    This method handles transaction network generation using local database.
    """
    print('#' * 60)
    bitGenerator = networkGenerator.NetworkGenerator()
    bitGenerator.generateLocalNetwork(address, layer)


def generateNetworkInternet(address, layer):
    """
    This method handles transaction network generation using Internet.
    """


def generateAddressGraph():
    """
    This method handles address centered transaction graph generation.
    """
    print('#' * 60)
    bitGenerator = networkGenerator.NetworkGenerator()
    bitGenerator.generateAddressCenteredGraph()


def generateFullEntityGraph():
    """
    This method handles entity centered transaction graph - full version generation.
    """
    print('#' * 60)
    bitGenerator = networkGenerator.NetworkGenerator()
    bitGenerator.generateFullEntityCenteredGraph()


def generateSimpleEntityGraph():
    """
    This method handles entity centered transaction graph - simplified version generation.
    """
    print('#' * 60)
    bitGenerator = networkGenerator.NetworkGenerator()
    bitGenerator.generateSimpleEntityCenteredGraph()


def programExit():
    """
    This method handles program exiting.
    """
    print('#' * 60)
    print("Good bye! -VisualBit V1.0")
    print('#' * 60)
    exit()


while choice != '0':
    print('#' * 60 + """
    Menu
        -1. Parse bitcoin blockchain files & construct databases
        -2. Delete all of the constructed databases
        -3. Cluster addresses of joint control
        -4. Generate transaction network
        -5. Generate transaction graph using the generated network
        -0. Exit""")
    choice = input("> [0-5]: ")
    print("")
    if choice == '0':
        # exit the program
        choice = '-1'
        while choice != '1' and choice != '2':
            print('#' * 60)
            print("""
            Are you sure to exit?
                -1. YES
                -2. NO""")
            choice = input("> [1-2]: ")
            if choice == '1':
                programExit()
                break
            elif choice == '2':
                break
            else:
                print("Invalid input! [1-2]")
    elif choice == '1':
        # parse raw blk data
        choice = '-1'
        while choice != '1' and choice != '2':
            print('#' * 60)
            print("""
            This process is very slow due to the massive I/O operations for database.
            It is recommended to use the constructed databases on the project website.
            Please put the .dat files in the directory example_bitcoin_data.
            Are you sure to continue?
                -1. YES
                -2. NO""")
            choice = input("> [1-2]: ")
            if choice == '1':
                parseData()
                break
            elif choice == '2':
                break
            else:
                print("Invalid input! [1-2]")
    elif choice == '2':
        # delete databases
        choice = '-1'
        while choice != '1' and choice != '2':
            print('#' * 60)
            print("""
            All of the tables will be dropped and transaction data will be deleted.
            Are you sure to continue?
                -1. YES
                -2. NO""")
            choice = input("> [1-2]: ")
            if choice == '1':
                deleteData()
                break
            elif choice == '2':
                break
            else:
                print("Invalid input! [1-2]")
    elif choice == '3':
        # cluster addresses
        choice = '-1'
        while choice != '1' and choice != '2':
            print('#' * 60)
            print("""
            This process is very slow due to the massive I/O operations for cluster database.
            It is recommended to use the constructed databases on the project website.
            Please make sure a database containing transaction info is already constructed.
            Are you sure to continue?
                -1. YES
                -2. NO""")
            choice = input("> [1-2]: ")
            if choice == '1':
                clusterAddress()
                break
            elif choice == '2':
                break
            else:
                print("Invalid input! [1-2]")
    elif choice == '4':
        # generate transaction network
        choice = '-1'
        while choice != '1' and choice != '2':
            print('#' * 60)
            print("""
            Please make sure a database containing transaction info is already constructed.
            The range of network depends on how complete the database is constructed.
            Are you sure to continue?
                -1. YES
                -2. NO""")
            choice = input("> [1-2]: ")
            if choice == '1':
                # generate transaction network using local database
                # because the provided database is only partial constructed, the address must be in the database
                # address example to explore: 13mpcjvzR4g4enTUYuw6LRb51UgF9P21Ut
                while True:
                    print('#' * 60)
                    print("""
                Generating the whole network would be too large and hard to inspect.
                Please enter a valid bitcoin address as the network center.
                Enter 0 to go back.""")
                    address = input("> ")
                    try:
                        is_valid = classHelper.validateAddress(address)
                    except Exception:
                        is_valid = False
                    if address == '0':
                        break
                    elif is_valid:
                        while True:
                            print('#' * 60)
                            layer = input("""
                Please enter the level of layers around the center address (the farthest node away from the center)
                An integer > 0, recommended to be <= 5.
> [1-5]: """)
                            layer = int(layer)
                            if layer > 0:
                                break
                        generateNetworkLocal(address, layer)
                        break
                    else:
                        print("Invalid address.")
            elif choice == '2':
                break
            else:
                print("Invalid input! [1-2]")
    elif choice == '5':
        # generate transaction graph
        choice = '-1'
        while choice != '1' and choice != '2':
            print('#' * 60)
            print("""
            !!!!!!                                              Warning                                             !!!!!!
            !!!!!!                        Please generate network first before using this function                  !!!!!!
            !!!!!!                                   Otherwise there will be no output                              !!!!!!
            
            There are two methods for transaction graph generation.
            Which one do you prefer?                - Please make sure a transaction network is already constructed
            
                -1.  Address centered               - Addresses as nodes connecting to each other (transactions)
                
                -2.1 Entity centered (full-version) - Tags (entities) as nodes connecting to each other (transactions)
                                                    - Addresses as small nodes connect to the entity node (belong to)
                                                    - This version includes all addresses of the entities as nodes
                                                    - It may be too large to display properly (too many nodes)
                                                    - If so, please use the simplified version
                                                    - Some entity may be isolated because not all addresses have tags
                                                    - Their related addresses therefore not rendered
                                                    - Basically not recommended
                                                    
                -2.2 Entity centered (simplified)   - Tags (entities) as nodes connecting to each other (transactions)
                                                    - Addresses as small nodes connect to the entity node (belong to)
                                                    - This version includes only the addresses related to the transactions
                                                    - Recommended, smaller and faster to display
                -3. Back""")
            choice = input("> [1-3]: ")
            if choice == '1':
                # generate address centered graph
                generateAddressGraph()
                break
            elif choice == '2.1':
                generateFullEntityGraph()
                break
            elif choice == '2.2':
                generateSimpleEntityGraph()
                break
            elif choice == '3':
                break
            else:
                print("Invalid input! [1-3]")
    else:
        print("Invalid input! [0-5]")
