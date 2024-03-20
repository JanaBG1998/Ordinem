import sqlite3

with sqlite3.connect('inv.db') as conn:
    c = conn.cursor()


    c.execute('''CREATE TABLE IF NOT EXISTS buch 
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    buchtitel TEXT NOT NULL)''')


'''c.execute("INSERT INTO buch (buchtitel)VALUES ('Harry Potter')")

c.execute("INSERT INTO buch (buchtitel)VALUES ('Potter Harry')")
'''

c.execute("DELETE FROM buch")
conn.commit()




def printDb(db):
    c.execute("SELECT * FROM buch")
    rows=c.fetchall()

    for row in rows:
        print(row)


printDb('buch')

c.close()

