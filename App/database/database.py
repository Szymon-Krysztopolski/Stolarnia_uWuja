DB_NAME = "database/Stolarnia.db"

connection = None
cursor = None

def MyQuery(q,vars=-1):
    try:
        if vars==-1:
            data = cursor.execute(q)
        else:
            data = cursor.execute(q,vars)
        connection.commit()
        return data
    except (connection.Error, connection.Warning) as e:
        print(e)
        return None
    
class Rodzaje_produktow():
    def create_table():
        table_script = '''CREATE TABLE IF NOT EXISTS Rodzaje_produktow(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        nazwa TEXT not null UNIQUE
                    );
                    '''
        MyQuery(table_script)

    def insert_record(nazwa):
        MyQuery('INSERT INTO Rodzaje_produktow(nazwa) VALUES(?)',(nazwa,))
        
    def update_record(id,nazwa):
        MyQuery('UPDATE Rodzaje_produktow SET nazwa=? WHERE ID=?',(nazwa,id))
    
    def get_id_by_name(nazwa):
        res = MyQuery('SELECT ID FROM Rodzaje_produktow WHERE nazwa=?',(nazwa,)).fetchone()
        
        if res is not None:
            return res[0]
        else:
            print("Error with query")
            return None
    
    def get_name_by_id(id):
        res = MyQuery('SELECT nazwa FROM Rodzaje_produktow WHERE ID=?',(id,)).fetchone()
        if res is not None:
            return res[0]
        else:
            print("Error with query")
            return None
        
class Rodzaje_materialow():
    def create_table():
        table_script = '''CREATE TABLE IF NOT EXISTS Rodzaje_materialow(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        nazwa TEXT not null UNIQUE,
                        cena_za_jednostke INTEGER not null
                    );
                    '''
        MyQuery(table_script)

    def insert_record(nazwa,cena):
        MyQuery('INSERT INTO Rodzaje_materialow(nazwa,cena_za_jednostke) VALUES(?,?)',(nazwa,cena))
        
    def update_record(id,nazwa,cena):
        MyQuery('UPDATE Rodzaje_materialow SET nazwa=?, cena_za_jednostke=? where ID=?',(nazwa,cena,id))
        
    def get_id_by_name(nazwa):
        res = MyQuery('SELECT ID FROM Rodzaje_materialow WHERE nazwa=?',(nazwa,)).fetchone()
        
        if res is not None:
            return res[0]
        else:
            print("Error with query")
            return None
        
class Produkty():
    def create_table():
        table_script = '''CREATE TABLE IF NOT EXISTS Produkty(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        ID_rodzaje_prod INTEGER not null,
                        nazwa TEXT not null UNIQUE,
                        cena_robocizna INTEGER not null,
                        FOREIGN KEY(ID_rodzaje_prod) REFERENCES Rodzaje_produktow(ID)
                    );
                    '''
        MyQuery(table_script)

    def insert_record(ID_rodzaje_prod,nazwa,cena_robocizna):
        MyQuery('INSERT INTO Produkty(ID_rodzaje_prod,nazwa,cena_robocizna) VALUES(?,?,?)',(ID_rodzaje_prod,nazwa,cena_robocizna))

    def update_record(id,id_pt,nazwa,cena):
        MyQuery('UPDATE Produkty SET ID_rodzaje_prod=?, nazwa=?, cena_robocizna=? where ID=?',(id_pt,nazwa,cena,id))

class Komponenty():
    def create_table():
        table_script = '''CREATE TABLE IF NOT EXISTS Komponenty(
                        ID_produktu INTEGER not null,
                        ID_materialu INTEGER not null,
                        nazwa TEXT not null,
                        wymiar_X INTEGER not null,
                        wymiar_Y INTEGER not null,
                        wymiar_Z INTEGER not null,
                        FOREIGN KEY(ID_produktu) REFERENCES Rodzaje_produktow(ID) on delete cascade,
                        FOREIGN KEY(ID_materialu) REFERENCES Rodzaje_materialow(ID),
                        PRIMARY KEY(ID_produktu,nazwa)
                    );
                    '''
        MyQuery(table_script)
        
    def insert_record(ID_produktu,ID_materialu,nazwa,wymiar_X,wymiar_Y,wymiar_Z):
        MyQuery('INSERT INTO Komponenty(ID_produktu,ID_materialu,nazwa,wymiar_X,wymiar_Y,wymiar_Z) VALUES(?,?,?,?,?,?)',
                (ID_produktu,ID_materialu,nazwa,wymiar_X,wymiar_Y,wymiar_Z))
        
    def fetch_records_by_prodID(id):
        return MyQuery(f"SELECT * FROM Komponenty where ID_produktu={id}")
    
    def del_record_byID(id1, id2, name):
        MyQuery("DELETE FROM Komponenty where ID_produktu=? and ID_materialu=? and nazwa=?",(id1, id2, name))

def fetch_records(table):
    return MyQuery(f"SELECT * FROM {table}")

def del_record_byID(table,id):
    MyQuery(f"DELETE FROM {table} where id={id}")

def database_init():
    Rodzaje_produktow.create_table()
    Rodzaje_materialow.create_table()
    Produkty.create_table()
    Komponenty.create_table()
    
def database_hard_reset():
    try:
        database_init()
        cursor.execute("DROP TABLE Rodzaje_produktow")
        cursor.execute("DROP TABLE Rodzaje_materialow")
        cursor.execute("DROP TABLE Produkty")
        cursor.execute("DROP TABLE Komponenty")
        database_init()
        connection.commit()
    except (connection.Error, connection.Warning) as e:
        print(e)
        return None