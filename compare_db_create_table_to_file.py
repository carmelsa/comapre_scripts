import json

import mysql.connector
import re


def connect_db(params):
    return mysql.connector.connect(
        host=params["host"],
        user=params["user"],
        password=params["password"],
        database=params["database"]
    )


ignore_spaces = False


def get_table_names_from_db(my_db):
    my_cursor = my_db.cursor()
    my_cursor.execute("SHOW TABLES")
    tables = my_cursor.fetchall()
    tables = [table for table, in tables]
    return tables


def get_table_names_from_file(content):
    table_names = []
    for match in re.finditer(r"CREATE TABLE\s*(IF NOT EXISTS)?\s*(`)?(?P<table_names>\w+)", content):
        table_names.append(match.group("table_names"))
    return table_names


def get_table_content_by_name_from_file(content):
    table_content_by_name = {}
    for match in re.finditer(r"CREATE TABLE\s*(IF NOT EXISTS)?\s*(`)?(?P<table_name>\w+)(`)?(?P<content>.*?);", content,
                             flags=re.DOTALL):
        table_content_by_name[match.group("table_name")] = match.group("content")
    return table_content_by_name


def get_table_content_by_name_from_db(my_db, table_name):
    my_cursor = my_db.cursor()
    my_cursor.execute("SHOW CREATE TABLE " + table_name)
    table_content = my_cursor.fetchall()
    return re.findall(r"CREATE TABLE\s*`\w+`\s+(?P<content>.*)", table_content[0][1], flags=re.DOTALL)


def compare_content(table_content_db, table_content_file, table_name):
    table_content_db_lines = [line.strip() for line in table_content_db.split("\n")]
    table_content_file_lines = [line.strip() for line in table_content_file.split("\n")]
    start = "**************************************\nfound difference in create table " + table_name + ":\n"
    find_diff(table_content_db_lines, table_content_file_lines, start)


def is_diff_spaces(set_db, set_file):
    if ignore_spaces and len(set_db) != 0 and len(set_file) != 0:
        text1 = [x.replace(' ', '') for x in set_db]
        text2 = [x.replace(' ', '') for x in set_file]
        return set(text1) ^ set(text2)


def find_diff(set_db, set_file, start):
    diff_from_db = set(set_db) - set(set_file)
    diff_from_file = set(set_file) - set(set_db)
    if is_diff_spaces(set_db, set_file):
        return
    if diff_from_db or diff_from_file:
        print(start)
    if diff_from_db:
        print("In db   - " + str(diff_from_db))
    if diff_from_file:
        print("In file - " + str(diff_from_file))


if __name__ == '__main__':
    f = open("compare_db_table_to_file.json", "r")
    params = json.load(f)
    ignore_spaces = params["ignore_spaces"]
    with open(params["create_table_file_path"], "r") as fd:
        content = fd.read()
    file_tables = get_table_names_from_file(content)
    my_db = connect_db(params)
    db_tables = get_table_names_from_db(my_db)
    find_diff(db_tables, file_tables, "missing tables :")
    table_content_by_name = get_table_content_by_name_from_file(content)
    for table_name in file_tables:
        table_content_db = get_table_content_by_name_from_db(my_db, table_name)
        compare_content(table_content_db[0], table_content_by_name.get(table_name), table_name)
    print("done")
