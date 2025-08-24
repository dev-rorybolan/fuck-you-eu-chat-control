from db import Database

database: Database = Database()

print(database.load_messages(channel='/general'))