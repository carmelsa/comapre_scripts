import sys
import mysql.connector
import ssl


def connect_db(host, user, password):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="kaltura",
        ssl_ca='',
        ssl_version=ssl.PROTOCOL_TLSv1_2
    )


def get_table_names_from_db(my_db):
    my_cursor = my_db.cursor()
    my_cursor.execute("SHOW TABLES")
    tables = my_cursor.fetchall()
    tables = [table for table, in tables]
    return tables


def main(argv):
    host = argv[0]
    user = argv[1]
    password = argv[2]
    my_db = connect_db(host, user, password)
    table = get_table_names_from_db(my_db)
    print(table)


if __name__ == '__main__':
    main(sys.argv[1:])
