import abc
from collections import defaultdict

TYPE = "type"
NAME = "name"
PARTNER_ID = "partnerid"
OBJECT_FIELD = "object"
SERVICE_FIELD = "service"


class Permission(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def print_item(self, item):
        string_to_print = ""
        if item.get(
                OBJECT_FIELD) is not None: string_to_print += '\033[97m' + "object\service: " + '\033[95m' + item.get(
            OBJECT_FIELD) + ", "
        if item.get(
                "parameter") is not None: string_to_print += '\033[97m' + "parameter: " + '\033[95m' + item.get(
            "parameter") + ", "
        if item.get("action") is not None: string_to_print += '\033[97m' + "action: " + '\033[95m' + item.get(
            "action") + ", "
        if item.get(PARTNER_ID) is not None: string_to_print += '\033[97m' + PARTNER_ID + ": " + '\033[95m' + str(
            item.get(PARTNER_ID)) + ", "
        if item.get("type") is not None: string_to_print += '\033[97m' + "type: " + '\033[95m' + str(
            item.get("type"))
        return string_to_print + '\033[0m'

    @abc.abstractmethod
    def convert_file_to_dict(self, file):
        pass

    @abc.abstractmethod
    def convert_db_to_dict(self, db_dict):
        pass

    def get_permission_from_db(self, my_db, query):
        my_cursor = my_db.cursor(dictionary=True)
        my_cursor.execute(query)
        permission_item_list = my_cursor.fetchall()
        return permission_item_list

    def get_file_permissions_dict(self, section, config, key_field):
        file_permissions_dict = defaultdict(dict)
        for option in config.options(section):
            split_option = option.replace(SERVICE_FIELD, OBJECT_FIELD).split(".")
            file_permissions_dict[split_option[0]][split_option[1]] = config.get(section, option)
        objects = {dict_item.get(key_field, dict_item.get(SERVICE_FIELD)) for dict_item in
                   file_permissions_dict.values()}
        return file_permissions_dict, set(objects)

    def str_item(self,file_item):
        return file_item.get(OBJECT_FIELD, "") + " " + file_item.get("parameter", "") + " " + file_item.get(
            "action", "") + " " + str(file_item.get(PARTNER_ID)) + " " + str(file_item.get("type", ""))
