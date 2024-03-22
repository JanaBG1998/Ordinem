import sqlite3

# Verbindung zur Datenbank herstellen (falls nicht vorhanden, wird sie erstellt)
conn = sqlite3.connect('inventar.db')

# Cursor-Objekt erstellen
cursor = conn.cursor()

# Tabelle für Räume erstellen
cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )''')

# Tabelle für Gegenstände erstellen
cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    price REAL NOT NULL,
                    weight REAL NOT NULL,
                    color TEXT,
                    expiry_date DATE,
                    room_id INTEGER,
                    FOREIGN KEY (room_id) REFERENCES rooms (id)
                )''')
'''SQLite does not have a storage class set aside for storing dates and/or times. Instead, the built-in Date And Time Functions of SQLite are capable of storing dates and times as TEXT, REAL, or INTEGER values:

TEXT as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS").
REAL as Julian day numbers, the number of days since noon in Greenwich on November 24, 4714 B.C. according to the proleptic Gregorian calendar.
INTEGER as Unix Time, the number of seconds since 1970-01-01 00:00:00 UTC.
Applications can choose to store dates and times in any of these formats and freely convert between formats using the built-in date and time functions.'''
# Änderungen speichern
conn.commit()

# Testdaten einfügen
cursor.execute("INSERT INTO rooms (name) VALUES ('Aldi')")
cursor.execute("INSERT INTO rooms (name) VALUES ('Rewe')")

# Beispiel: Gegenstände hinzufügen
cursor.execute("INSERT INTO items (name, amount, price, weight, color, expiry_date, room_id) VALUES (?, ?, ?, ?, ?, ?, ?)", ('Milch', 10, 1.99, 1.5, 'Weiß', '2024-03-31', 1))
cursor.execute("INSERT INTO items (name, amount, price, weight, color, expiry_date, room_id) VALUES (?, ?, ?, ?, ?, ?, ?)", ('Käse', 5, 3.49, 0.3, 'Gelb', '2024-04-10', 1))
cursor.execute("INSERT INTO items (name, amount, price, weight, color, expiry_date, room_id) VALUES (?, ?, ?, ?, ?, ?, ?)", ('Fisch', 3, 7.99, 0.8, 'Rot', '2024-03-25', 2))

# Änderungen speichern
conn.commit()
"""
# Funktion zum Hinzufügen eines Gegenstands zu einer Inventarliste
def add_item_to_inventory(item_name, room_id):
    cursor.execute("INSERT INTO items (name, room_id) VALUES (?, ?)", (item_name, room_id))
    conn.commit()

# Beispiel: Gegenstände hinzufügen
add_item_to_inventory('Brot', 1)
add_item_to_inventory('Apfel', 1)
"""

conn.commit()

def show_inventory():
    cursor.execute("SELECT items.id, items.name AS item_name, items.amount, items.price, items.weight, items.color, items.expiry_date, rooms.name AS room_name FROM items INNER JOIN rooms ON items.room_id = rooms.id")
    inventory = cursor.fetchall()
    for row in inventory:
        print(f"Item ID: {row[0]}, Item Name: {row[1]}, Amount: {row[2]}, Price: {row[3]}, Weight: {row[4]}, Color: {row[5]}, Expiry Date: {row[6]}, Room Name: {row[7]}")

# Beispiel: Inhalte der Datenbank anzeigen
show_inventory()

# Datenbankverbindung schließen
conn.close()