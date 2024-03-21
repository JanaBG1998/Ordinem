import sqlite3


def printDb(c):
    c.execute("SELECT * FROM buch")
    rows = c.fetchall()

    for row in rows:
        print(row)


with sqlite3.connect('inv.db') as conn:
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Inventar
    (room_id INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS itemlist
    (item_id INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, room_id INTEGER,FOREIGN KEY (room_id) REFERENCES rooms (id))''')



'''c.execute("INSERT INTO Inventar (ID,name) VALUES (30,'Penny')")'''

c.execute("INSERT INTO Inventar (name) VALUES ('ALDI')")
c.execute("INSERT INTO Inventar (name) VALUES ('REWE')")



'''c.execute("DELETE FROM INVENTAR")'''
conn.commit()



