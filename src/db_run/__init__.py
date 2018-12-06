from psycopg2 import connect
from psycopg2.extras import RealDictCursor


class DB:
    username = "postgres"
    passwd = "coderslab"
    hostname = "localhost"
    db = "warsztaty_db"

    def clean(self):
        sql = "DROP DATABASE IF EXISTS warsztaty_db;"
        cnx = connect(user=self.username, password=self.passwd, host=self.hostname)
        cnx.autocommit = True
        with cnx.cursor() as curs:
            curs.execute(sql)
        cnx.close()

    def run(self):
        sql = "CREATE DATABASE warsztaty_db;"
        cnx = connect(user=self.username, password=self.passwd, host=self.hostname)
        cnx.autocommit = True
        with cnx.cursor() as curs:
            curs.execute(sql)
        cnx.close()
        print('Database created')

    def connect_db(self):
        self.cnx = connect(user=self.username, password=self.passwd, host=self.hostname, database=self.db)
        return self.cnx

    def db_cursor(self, connection):
        self.cursor = connection.cursor(cursor_factory=RealDictCursor)
        return self.cursor

    def create_tables(self, cursor):
        sql_u = '''CREATE TABLE users (id serial, username varchar(100) not NULL UNIQUE ,
                   email varchar(150) not NULL UNIQUE , hashed_password VARCHAR(150) not NULL, PRIMARY KEY (id));'''
                   #nazwa tabeli user jest niedozwolona przez postgresql
        sql_m = '''CREATE TABLE message (id serial, from_id INTEGER, to_id INTEGER,
                   Text VARCHAR(255), creation_date TIMESTAMP, PRIMARY KEY (id), FOREIGN key(from_id) REFERENCES users(id) on DELETE CASCADE,
                   FOREIGN key(to_id) REFERENCES users(id) on DELETE CASCADE);'''
        try:
            cursor.execute(sql_u)
            cursor.execute(sql_m)
            print('tables created')
        except Exception:
            raise Exception
