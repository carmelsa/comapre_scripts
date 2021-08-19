import configparser
import glob
import json
import re
from collections import defaultdict
from copy import deepcopy

import mysql.connector

OBJECT_FIELD = "object"
SERVER_FIELD = "service"
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
            permissions_names = file_permission.get("permissions").split(",")
            del (file_permissions_delete[key])
            return {re.search(r"\s*(.*?>)?(?P<content>.*)\s*", x).group("content") for x in permissions_names}

    file_error_message.append("missing configuration in file . db has permission - " + str_item(db_permission))


def find_diff_in_names(permission_names_from_db, permission_names_from_file, db_item, file_error_message):
    if not permission_names_from_db or not permission_names_from_file:
        return
    diff_from_db = permission_names_from_db - permission_names_from_file
    diff_from_file = permission_names_from_file - permission_names_from_db
    if diff_from_db or diff_from_file:
        file_error_message.append(
            "******************* found diff in permissions " + str_item(db_item) + " : *******************")
    if diff_from_db:
        file_error_message.append("In db   - " + str(diff_from_db))
    if diff_from_file:
        file_error_message.append("In file - " + str(diff_from_file))


def str_item(file_item):
    return file_item.get(OBJECT_FIELD) + " " + file_item.get("parameter", "") + " " + file_item.get(
        "action") + " " + str(
        file_item.get("partnerid"))


def get_file_permissions_dict(section, config, file_error_message):
    file_permissions_dict = defaultdict(dict)
    for option in config.options(section):
        split_option = option.replace("service", OBJECT_FIELD).split(".")
        file_permissions_dict[split_option[0]][split_option[1]] = config.get(section, option)
    objects = {dict_item.get(OBJECT_FIELD, dict_item.get("service")) for dict_item in file_permissions_dict.values()}
    if len(objects) != 1:
        file_error_message.append("more than 1 object in file")
    return file_permissions_dict, objects.pop()


def compare_db_to_file_permissions(my_db, path):
    file_error_message = []
    config = configparser.ConfigParser()
    config.read(path)
    for section in config.sections():
        if section == "action_permission_items":
            compare_section_permissions(config, my_db, section, SELECT_WITH_JOIN_ACTION, file_error_message)
        elif section == "parameter_permission_items":
            compare_section_permissions(config, my_db, section, SELECT_WITH_JOIN_PARAMETER, file_error_message)
        else:
            file_error_message.append("unknown file type " + section)
            continue
    if len(file_error_message) != 0:
        print('\033[94m' + "\nfile : " + path + '\033[0m')
        [print(x) for x in file_error_message]


def compare_section_permissions(config, my_db, section, select_query, file_error_message):
    file_permissions_dict, object_name = get_file_permissions_dict(section, config, file_error_message)
    db_permission_dict = get_permission_from_db(my_db, object_name, select_query)
    file_permissions_delete = deepcopy(file_permissions_dict)

    for db_item in db_permission_dict:
        permission_names_from_db = set(db_item.get("permissions").split(","))
        permission_names_from_file = get_permission_names_from_file(db_item, file_permissions_dict,
                                                                    file_permissions_delete, file_error_message)
        find_diff_in_names(permission_names_from_db, permission_names_from_file, db_item, file_error_message)
    if len(file_permissions_delete) != 0:
        for file_permission in file_permissions_delete.values():
            file_error_message.append(
                "missing configuration in db . file has permission - " + str_item(file_permission))


def main():
    with open("compare_db_table_to_file.json", "r") as f:
        params = json.load(f)
    my_db = connect_db(params)

    folder_path = params.get("permission_folder_path")
    if folder_path:
        for path in glob.glob(folder_path + "/*.ini"):
            compare_db_to_file_permissions(my_db, path)
    elif params.get("permission_file_path"):
        compare_db_to_file_permissions(my_db, params["permission_file_path"])
    else:
        print("please specify the file/folder path")
        exit(0)
    print("done")


if __name__ == '__main__':
    main()
