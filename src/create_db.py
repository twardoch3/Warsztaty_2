#!/usr/bin/python3

from db_run import DB

# create Database and tables users and messages
if __name__ == '__main__':
    o = DB()
    o.clean()
    o.run()
    connection = o.connect_db()

    with o.db_cursor(connection) as curs:
        o.create_tables(curs)
        print(curs)
    print(curs)

    print(connection)
    connection.commit()
    connection.close()
    print(connection)
