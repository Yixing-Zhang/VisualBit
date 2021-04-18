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
