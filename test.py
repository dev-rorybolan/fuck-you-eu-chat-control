from database import Database

database: Database = Database()

print(database.get_messages(channel='/general'))