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
                        nazwa VARCHAR(50) not null
                    );
                    '''
        MyQuery(table_script)

    def insert_record(nazwa):
        MyQuery('INSERT INTO Rodzaje_produktow(nazwa) VALUES(?)',(nazwa,))
        
    def update_record(id,nazwa):
        MyQuery('UPDATE Rodzaje_produktow SET nazwa = ? where ID= ?',(nazwa,id))
        
class Rodzaje_materialow():
    def create_table():
        table_script = '''CREATE TABLE IF NOT EXISTS Rodzaje_materialow(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        nazwa VARCHAR(50) not null,
                        cena_za_jednostke number(10) not null
                    );
                    '''
        MyQuery(table_script)

    def insert_record(nazwa,cena):
        MyQuery('INSERT INTO Rodzaje_materialow(nazwa,cena_za_jednostke) VALUES(?,?)',(nazwa,cena))
        
    def update_record(id,nazwa,cena):
        MyQuery('UPDATE Rodzaje_materialow SET nazwa=?, cena_za_jednostke=? where ID=?',(nazwa,cena,id))
        
def fetch_records(table):
    return MyQuery(f"SELECT * FROM {table}")

def del_record_byID(table,id):
    MyQuery(f"DELETE FROM {table} where id={id}")

def database_init():
    Rodzaje_produktow.create_table()
    Rodzaje_materialow.create_table()
    
def database_hard_reset():
    try:
        cursor.execute("DROP TABLE Rodzaje_produktow")
        cursor.execute("DROP TABLE Rodzaje_materialow")
        connection.commit()
    except (connection.Error, connection.Warning) as e:
        print(e)
        return None