import sqlite3
conn = sqlite3.connect("coordinates.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM points;")
print(cursor.fetchall())
conn.close()
