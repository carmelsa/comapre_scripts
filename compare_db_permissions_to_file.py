import configparser
import glob
import json
import re
from collections import defaultdict
from copy import deepcopy

import mysql.connector
from permissions_type.permission import Permission
from permissions_type.permission_action import PermissionAction
from permissions_type.permission_parameter import PermissionParameter
from permissions_type.permission_partner_id import PermissionPartnerId

import permissions_type

TYPE = "type"
NAME = "name"
PARTNER_ID = "partnerid"
OBJECT_FIELD = "object"
SERVICE_FIELD = "service"


def connect_db(params):
    return mysql.connector.connect(
        host=params["host"],
        user=params["user"],
        password=params["password"],
        database=params["database"]
    )


def get_permission_names_from_file(permission_object, db_permission, file_permissions_dict, file_permissions_delete,
                                   file_error_message):
    for key, file_permission in file_permissions_dict.items():
        if permission_object.str_item(file_permission).lower() == permission_object.str_item(db_permission).lower():
            permissions_names = file_permission.get("permissions", file_permission.get("name")).split(",")
            del (file_permissions_delete[key])
            return {re.search(r"\s*(.*?>)?(?P<content>.*)\s*", x).group("content") for x in permissions_names}

    file_error_message.append(
        '\033[94m' + "In db   - " + '\033[0m' + permission_object.print_item(db_permission) + " file does not have it!")


def find_diff_in_names(permission_object, permission_names_from_db, permission_names_from_file, db_item):
    if not permission_names_from_db or not permission_names_from_file:
        return
    diff_from_db = permission_names_from_db - permission_names_from_file
    diff_from_file = permission_names_from_file - permission_names_from_db
    return get_diff_error_message(permission_object, db_item, diff_from_db, diff_from_file)


def get_diff_error_message(permission_object, db_item, diff_from_db, diff_from_file):
    error_message = ""
    if diff_from_db or diff_from_file:
        error_message += "*********************************************\n" + '\033[96m' + "found diff in permissions " + '\033[0m' + "with " + permission_object.print_item(
            db_item) + ":\n"
        error_message += '\033[94m' + "In db   - " + '\033[0m' + str(diff_from_db)
        error_message += '\n\033[94m' + "In file - " + '\033[0m' + str(diff_from_file)
        error_message += "\n*********************************************\n"
    return error_message


def check_section_type(section):
    if section == "action_permission_items":
        return permissions_type.permission_action.PermissionAction()
    elif section == "parameter_permission_items":
        return permissions_type.permission_parameter.PermissionParameter()
    elif section == "permissions":
        return permissions_type.permission_partner_id.PermissionPartnerId()
    return None


def compare_db_to_file_permissions(my_db, path):
    file_error_message = []
    diff_error_message = []
    error_message = []
    config = configparser.ConfigParser()
    config.read(path)
    for section in config.sections():
        permission_object = check_section_type(section)
        if permission_object is None:
            error_message.append("Unknown file type " + section)
            continue
        file_permissions_dict, key_objects = permission_object.get_file_permissions_dict(section, config)
        for key_object in key_objects:
            db_permission_dict = permission_object.get_permission_from_db(my_db, key_object)
            compare_section_permissions(permission_object, db_permission_dict, file_error_message, diff_error_message,
                                        file_permissions_dict,
                                        key_object)
    print_error_messages(diff_error_message, file_error_message, error_message, path)


def print_error_messages(diff_error_message, file_error_message, error_message, path):
    file_error_message = set(filter(None, file_error_message))
    error_message = set(filter(None, error_message))
    diff_error_message = set(filter(None, diff_error_message))
    if len(file_error_message) != 0 or len(diff_error_message) != 0 or len(error_message) != 0:
        print('\033[93m' + "\nfile : " + path + '\033[0m')
        if len(error_message) != 0:
            [print('\033[96m' + x) for x in error_message]
            print("")
        if len(file_error_message) != 0:
            print('\033[96m' + "missing configuration:" + '\033[0m')
            [print(x) for x in file_error_message]
            print("")
        if len(diff_error_message) != 0:
            [print(x) for x in diff_error_message]


def compare_section_permissions(permission_object, db_permission_dict, file_error_message, diff_error_message,
                                file_permissions_dict,
                                object_name):
    file_permissions_delete = deepcopy(file_permissions_dict)
    for db_item in db_permission_dict.values():
        permission_names_from_db = set(db_item.get("permissions"))
        permission_names_from_file = get_permission_names_from_file(permission_object, db_item, file_permissions_dict,
                                                                    file_permissions_delete, file_error_message)
        diff_error_message.append(
            find_diff_in_names(permission_object, permission_names_from_db, permission_names_from_file, db_item))
    if len(file_permissions_delete) != 0:
        for file_permission in file_permissions_delete.values():
            if file_permission.get(OBJECT_FIELD) == object_name:
                file_error_message.append(
                    '\033[94m' + "In file   - " + '\033[0m' + permission_object.print_item(
                        file_permission) + " db does not have it!")


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
