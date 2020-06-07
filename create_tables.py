import sqlite3

# manual creation of database

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
# INTEGER for autoincrementing columns
create_table_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table_users)

create_table_items = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table_items)

connection.commit()
connection.close()
