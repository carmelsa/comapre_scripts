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
ignore_capital = False
ignore_auto_increment = False
ignore_default_null = False
ignore_int_and_tiny_int = False


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
    start = "found difference in create table " + table_name + ":\n"
    find_diff(table_content_db_lines, table_content_file_lines, start)


def check_ignores(line):
    if ignore_capital:
        line = line.lower()
    if ignore_auto_increment:
        line = re.sub(r'auto_increment(=\d*)?', '', line)
    if ignore_default_null:
        line = line.replace("default null", '')
    if ignore_spaces:
        line = line.replace(' ', '')
    if ignore_int_and_tiny_int:
        line = re.sub(r'int\(\d*\)', '', line)
        line = re.sub(r'tinyint\(\d*\)', '', line)

    return line


def check_if_diff_ignored(set_db, set_file):
    if len(set_db) == 0 or len(set_file) == 0:
        return False
    test_db = [check_ignores(x) for x in set_db]
    test_file = [check_ignores(x) for x in set_file]
    return len(set(test_db) ^ set(test_file)) == 0


def find_diff(set_db, set_file, start):
    diff_from_db = set(set_db) - set(set_file)
    diff_from_file = set(set_file) - set(set_db)
    if check_if_diff_ignored(set_db, set_file):
        return
    if diff_from_db or diff_from_file:
        print("\n****************************************************************************\n")
        print('\033[96m' + start + '\033[0m')
    if diff_from_db:
        print('\033[94m' + "In db   - " + '\033[0m' + str(diff_from_db))
    if diff_from_file:
        print('\033[94m' + "In file - " + '\033[0m' + str(diff_from_file))


def main():
    params = load_param()
    base_path = params.get("base_path")
    with open(base_path + params["create_table_file_path"], "r") as fd:
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


def load_param():
    global ignore_spaces, ignore_capital, ignore_auto_increment, ignore_default_null, ignore_int_and_tiny_int
    f = open("compare_db_table_to_file.json", "r")
    params = json.load(f)
    ignore_spaces = params.get("ignore_spaces", False)
    ignore_capital = params.get("ignore_capital", False)
    ignore_auto_increment = params.get("ignore_auto_increment", False)
    ignore_default_null = params.get("ignore_default_null", False)
    ignore_int_and_tiny_int = params.get("ignore_int_and_tiny_int", False)
    return params


if __name__ == '__main__':
    main()
