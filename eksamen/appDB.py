import sqlite3
from sqlite3 import Error



def createDB_table(conn):
    cur = conn.cursor()
    try:
        usertable = ("CREATE TABLE Users ("
                     "userID INTEGER, "
                     "username VARCHAR(40) NOT NULL UNIQUE, "
                     "passwordhash VARCHAR(120) NOT NULL, "
                     "role TEXT, "
                     "PRIMARY KEY(userID))")
        cur.execute(usertable)

        brewerytable = ("CREATE TABLE Brewery ("
                        "breweryID INTEGER, "
                        "breweryName VARCHAR(40), "
                        "city VARCHAR(40), "
                        "PRIMARY KEY(breweryID))")
        cur.execute(brewerytable)

        beertable = ("CREATE TABLE Beer ("
                     "beerID INTEGER, "
                     "beerName VARCHAR(40) UNIQUE, "
                     "style VARCHAR(40), "
                     "breweryID INTEGER, "
                     "PRIMARY KEY(beerID), "
                     "FOREIGN KEY(breweryID) REFERENCES brewerytable(breweryID))")
        cur.execute(beertable)

    except sqlite3.Error as err:
        print("Error {}".format(err))
    else:
        print("Table Created")
    finally:
        cur.close()

def update_info(conn,beerName,style,breweryID,beerID):
    cur = conn.cursor()
    try:
        sql = ("UPDATE Beer SET beerName =?, style =?, breweryID =? WHERE beerID =?")
        a=cur.execute(sql,(beerName, style, breweryID, beerID,))
        conn.commit()
        return a.rowcount
    except sqlite3.Error as err:
        print("Error {}".format(err))
    finally:
        cur.close()

def add_user(conn, username, hash, role="user"):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO Users (username, passwordhash, role) VALUES (?,?,?)")
        cur.execute(sql, (username,hash,role))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} created with id {}".format(username, cur.lastrowid))
        print(cur.lastrowid)
        return cur.lastrowid
    finally:
        cur.close()

def delete_beer_by_id(conn, beerID):
    cur = conn.cursor()
    try:
        sql ="DELETE FROM Beer WHERE beerID=?"
        a = cur.execute(sql,(beerID,))
        conn.commit()
        return a.rowcount
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def add_beer(conn,beerName, style, breweryID):
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO Beer ( beerName, style, breweryID) VALUES (?,?,?)")
        cur.execute(sql, ( beerName, style,breweryID))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Beer {} added with id{}".format( beerName, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()

def get_beer(conn, beerID):
    cur = conn.cursor()
    sql = ("SELECT beerID, beerName, style, breweryID FROM Beer WHERE beerID =?")
    cur.execute(sql,(beerID,))

    for row in cur:

        return row

def get_brewery(conn,breweryID):
    cur = conn.cursor()
    sql = ("SELECT breweryID, breweryName FROM Brewery WHERE breweryID =?")
    cur.execute(sql,(breweryID,))
    for row in cur:
        return row


def get_user_by_name(conn, username):
    cur = conn.cursor()
    try:
        sql = ("SELECT userID, username, role FROM Users WHERE username = ?")
        cur.execute(sql, (username,))
        for row in cur:
            (id,name,role) = row
            return {
                "username": name,
                "userID": id,
                "role": role
            }
        else:
            return {
                "username": username,
                "userID": None,
                "role": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def get_hash_for_login(conn, username):
    cur = conn.cursor()
    try:
        sql = ("SELECT passwordhash FROM Users WHERE username=?")
        cur.execute(sql, (username,))
        for row in cur:
            (passhash,) = row
            return passhash
        else:
            return None
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

def insert_data(conn):
    cur = conn.cursor()

    beers = [('slam dunk','IPA', 1),('easy','IPA', 2),('bankshot','IPA', 1)]
    breweries = [('Salikatt','Stavanger'),('Lærvig','Stavanger'),('Cervesiam','Oslo'),
                 ('Jåttå Gårdsbryggeri','Stavanger'),('Rygr','Klepp')]

    breweryinsert = "INSERT INTO Brewery (breweryName, city) VALUES(?,?)"
    beerinsert = "INSERT INTO Beer (beerName, style, breweryID) VALUES(?,?,?)"

    try:

        cur.executemany(breweryinsert,breweries)
        cur.executemany(beerinsert,beers)
        conn.commit()

    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Rows inserted.")
    finally:
        cur.close()


def queryDB(conn):
    cur = conn.cursor()
    userquery = "SELECT username FROM Users"
    breweryquery = "SELECT * FROM Brewery"
    beerquery = "SELECT * FROM Beer"
    joinquery = "SELECT Beer.beerName, Brewery.breweryName FROM Beer" \
                " INNER JOIN Brewery ON Beer.breweryID = Brewery.breweryID"

    try:
        cur.execute(userquery)

        for i in cur:
            print("{}".format(i))

    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Query successful.")
    cur.close()


if __name__ == "__main__":
    try:
        conn = sqlite3.connect("Webpage.db")
    except Error as err:
        print(err)
    else:
        createDB_table(conn)
        insert_data(conn)
        conn.close()

