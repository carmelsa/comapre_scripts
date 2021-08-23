import configparser
import glob
import json
import re
from collections import defaultdict
from copy import deepcopy

import mysql.connector

TYPE = "type"
NAME = "name"
PARTNER_ID = "partnerid"
OBJECT_FIELD = "object"
SERVICE_FIELD = "service"
SELECT_WITH_JOIN_PARAMETER = r"""
select param_1 as object ,param_2 as parameter,param_3 as action,param_4,param_5 ,permission_item.partner_id as partnerid, 
GROUP_CONCAT(DISTINCT name) as permissions
from permission_item join permission_to_permission_item 
on permission_item.id=permission_to_permission_item.permission_item_id 
join permission on permission_to_permission_item.permission_id=permission.id 
where param_1="%s" and permission_item.type="kApiParameterPermissionItem"
Group by param_1,param_2,param_4,param_3,param_5,permission_item.partner_id"""

SELECT_WITH_JOIN_ACTION = r"""
select param_1 as object,param_2 as action,param_3,param_4,param_5 ,permission_item.partner_id as partnerid, 
GROUP_CONCAT(DISTINCT name) as permissions
from permission_item join permission_to_permission_item 
on permission_item.id=permission_to_permission_item.permission_item_id 
join permission on permission_to_permission_item.permission_id=permission.id 
where param_1="%s" and permission_item.type="kApiActionPermissionItem"
Group by param_1,param_2,param_4,param_3,param_5,permission_item.partner_id"""

SELECT_WITH_JOIN_PARTNER = r"""select permission_item.partner_id as partnerid, permission.type ,
GROUP_CONCAT(DISTINCT name) as permissions
from permission_item join permission_to_permission_item 
on permission_item.id=permission_to_permission_item.permission_item_id 
join permission on permission_to_permission_item.permission_id=permission.id 
where  permission_item.partner_id = %s Group by permission_item.partner_id, permission.type"""


def connect_db(params):
    return mysql.connector.connect(
        host=params["host"],
        user=params["user"],
        password=params["password"],
        database=params["database"]
    )


def get_permission_from_db(my_db, object_name, SELECT_WITH_JOIN):
    my_cursor = my_db.cursor(dictionary=True)
    my_cursor.execute(SELECT_WITH_JOIN % object_name)
    permission_item_list = my_cursor.fetchall()
    return permission_item_list


def get_permission_names_from_file(db_permission, file_permissions_dict, file_permissions_delete, file_error_message):
    for key, file_permission in file_permissions_dict.items():
        if str_item(file_permission).lower() == str_item(db_permission).lower():
            permissions_names = file_permission.get("permissions", file_permission.get("name")).split(",")
            del (file_permissions_delete[key])
            return {re.search(r"\s*(.*?>)?(?P<content>.*)\s*", x).group("content") for x in permissions_names}

    file_error_message.append(
        '\033[94m' + "In db   - " + '\033[0m' + print_item(db_permission) + "file does not have it!")


def find_diff_in_names(permission_names_from_db, permission_names_from_file, db_item):
    if not permission_names_from_db or not permission_names_from_file:
        return
    diff_from_db = permission_names_from_db - permission_names_from_file
    diff_from_file = permission_names_from_file - permission_names_from_db
    return get_diff_error_message(db_item, diff_from_db, diff_from_file)


def get_diff_error_message(db_item, diff_from_db, diff_from_file):
    error_message = ""
    if diff_from_db or diff_from_file:
        error_message += "*********************************************\n" + '\033[96m' + "found diff in permissions " + '\033[0m' + "with " + print_item(
            db_item) + ":\n"
        error_message += '\033[94m' + "In db   - " + '\033[0m' + str(diff_from_db)
        error_message += '\n\033[94m' + "In file - " + '\033[0m' + str(diff_from_file)
        error_message += "\n*********************************************\n"
    return error_message


def str_item(file_item):
    return file_item.get(OBJECT_FIELD, "") + " " + file_item.get("parameter", "") + " " + file_item.get(
        "action", "") + " " + str(file_item.get(PARTNER_ID)) + " " + str(file_item.get("type", ""))


def print_item(file_item):
    string_to_print = ""
    if file_item.get(
            OBJECT_FIELD) is not None: string_to_print += '\033[97m' + "object\service: " + '\033[95m' + file_item.get(
        OBJECT_FIELD) + ", "
    if file_item.get(
            "parameter") is not None: string_to_print += '\033[97m' + "parameter: " + '\033[95m' + file_item.get(
        "parameter") + ", "
    if file_item.get("action") is not None: string_to_print += '\033[97m' + "action: " + '\033[95m' + file_item.get(
        "action") + ", "
    if file_item.get(PARTNER_ID) is not None: string_to_print += '\033[97m' + PARTNER_ID + ": " + '\033[95m' + str(
        file_item.get(PARTNER_ID)) + ", "
    if file_item.get("type") is not None: string_to_print += '\033[97m' + "type: " + '\033[95m' + str(
        file_item.get("type"))
    return string_to_print + '\033[0m'


def create_partner_dict(file_permission, partner_dict):
    key = file_permission.get(PARTNER_ID) + "_" + file_permission.get(TYPE)
    partner_dict[key][PARTNER_ID] = file_permission.get(PARTNER_ID)
    partner_dict[key][TYPE] = file_permission.get(TYPE)
    partner_dict[key][NAME] = file_permission.get(NAME) if partner_dict[key].get(NAME) is None \
        else partner_dict[key][NAME] + "," + file_permission.get(NAME)


def get_file_permissions_dict(section, config, key_field):
    file_permissions_dict = defaultdict(dict)
    for option in config.options(section):
        split_option = option.replace(SERVICE_FIELD, OBJECT_FIELD).split(".")
        file_permissions_dict[split_option[0]][split_option[1]] = config.get(section, option)
    objects = {dict_item.get(key_field, dict_item.get(SERVICE_FIELD)) for dict_item in file_permissions_dict.values()}
    if key_field == PARTNER_ID:
        partner_dict = defaultdict(dict)
        {create_partner_dict(x, partner_dict) for x in file_permissions_dict.values()}
        return partner_dict, set(objects)
    return file_permissions_dict, set(objects)


def check_section_type(section):
    if section == "action_permission_items":
        return SELECT_WITH_JOIN_ACTION, OBJECT_FIELD
    elif section == "parameter_permission_items":
        return SELECT_WITH_JOIN_PARAMETER, OBJECT_FIELD
    elif section == "permissions":
        return SELECT_WITH_JOIN_PARTNER, PARTNER_ID
    return None, None


def compare_db_to_file_permissions(my_db, path):
    file_error_message = []
    diff_error_message = []
    error_message = []
    config = configparser.ConfigParser()
    config.read(path)
    for section in config.sections():
        query, key_field = check_section_type(section)
        if query is None or key_field is None:
            error_message.append("Unknown file type " + section)
            continue
        file_permissions_dict, key_objects = get_file_permissions_dict(section, config, key_field)
        for key_object in key_objects:
            compare_section_permissions(my_db, query, file_error_message, diff_error_message, file_permissions_dict,
                                        key_object)
    print_error_messages(diff_error_message, file_error_message, error_message, path)


def print_error_messages(diff_error_message, file_error_message, error_message, path):
    if len(file_error_message) != 0 or len(diff_error_message) != 0 or len(error_message) != 0:
        print('\033[93m' + "\nfile : " + path + '\033[0m')
        if len(error_message) != 0:
            [print('\033[96m' + x) for x in set(filter(None, error_message))]
            print("")
        if len(file_error_message) != 0:
            print('\033[96m' + "missing configuration:" + '\033[0m')
            [print(x) for x in set(filter(None, file_error_message))]
            print("")
        if len(diff_error_message) != 0:
            [print(x) for x in set(filter(None, diff_error_message))]


def compare_section_permissions(my_db, select_query, file_error_message, diff_error_message, file_permissions_dict,
                                object_name):
    db_permission_dict = get_permission_from_db(my_db, object_name, select_query)
    file_permissions_delete = deepcopy(file_permissions_dict)
    for db_item in db_permission_dict:
        permission_names_from_db = set(db_item.get("permissions").split(","))
        permission_names_from_file = get_permission_names_from_file(db_item, file_permissions_dict,
                                                                    file_permissions_delete, file_error_message)
        diff_error_message.append(find_diff_in_names(permission_names_from_db, permission_names_from_file, db_item))
    if len(file_permissions_delete) != 0:
        for file_permission in file_permissions_delete.values():
            if file_permission.get(OBJECT_FIELD) == object_name:
                file_error_message.append(
                    '\033[94m' + "In file   - " + '\033[0m' + print_item(
                        file_permission) + "db does not have it!")


def main():
    with open("compare_db_table_to_file.json", "r") as f:
        params = json.load(f)
    my_db = connect_db(params)
    base_path = params.get("base_path")
    folder_path = params.get("permission_folder_path")
    if folder_path:
        for path in glob.glob(base_path + folder_path + "/*.ini"):
            compare_db_to_file_permissions(my_db, path)
    elif params.get("permission_file_path"):
        compare_db_to_file_permissions(my_db, base_path + params["permission_file_path"])
    else:
        print("please specify the file/folder path")
        exit(0)
    print("done")


if __name__ == '__main__':
    main()
