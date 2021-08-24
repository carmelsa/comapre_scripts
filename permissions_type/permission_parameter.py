from abc import ABC
from collections import defaultdict

from permissions_type.permission import Permission

SELECT_QUERY = r"""
select param_1 as object ,param_2 as parameter,param_3 as action,param_4,param_5 ,permission_item.partner_id as partnerid, 
GROUP_CONCAT(DISTINCT name) as permissions
from permission_item join permission_to_permission_item 
on permission_item.id=permission_to_permission_item.permission_item_id 
join permission on permission_to_permission_item.permission_id=permission.id 
where param_1="%s" and permission_item.type="kApiParameterPermissionItem"
Group by param_1,param_2,param_4,param_3,param_5,permission_item.partner_id"""

TYPE = "type"
NAME = "name"
PARTNER_ID = "partnerid"
OBJECT_FIELD = "object"
SERVICE_FIELD = "service"


class PermissionParameter(Permission):
    def convert_file_to_dict(self, file):
        pass

    def convert_db_to_dict(self, db_dict):
        pass

    def print_item(self, item):
        string_to_print = ""
        if item.get(
                OBJECT_FIELD) is not None: string_to_print += '\033[97m' + "object: " + '\033[95m' + item.get(
            OBJECT_FIELD) + ", "
        if item.get(
                "parameter") is not None: string_to_print += '\033[97m' + "parameter: " + '\033[95m' + item.get(
            "parameter") + ", "
        if item.get("action") is not None: string_to_print += '\033[97m' + "action: " + '\033[95m' + item.get(
            "action") + ", "
        if item.get(PARTNER_ID) is not None: string_to_print += '\033[97m' + PARTNER_ID + ": " + '\033[95m' + str(
            item.get(PARTNER_ID)) + ", "
        return string_to_print + '\033[0m'

    def get_permission_from_db(self, my_db, object_name):
        query = SELECT_QUERY % object_name
        permission_item_list = super().get_permission_from_db(my_db, query)
        db_permissions_dict = self.convert_permission_db_list(permission_item_list)
        return db_permissions_dict

    def convert_permission_db_list(self, permission_item_list):
        db_permissions_dict = defaultdict(dict)
        for item in permission_item_list:
            key = item.get(OBJECT_FIELD) + "_" + item.get("parameter") + "_" + item.get("action")
            item["permissions"] = item.get("permissions").split(",")
            db_permissions_dict[key] = item
        return db_permissions_dict

    def get_file_permissions_dict(self, section, config):
        file_permissions_dict, objects = super().get_file_permissions_dict(section, config, OBJECT_FIELD)
        return file_permissions_dict, objects

    def str_item(self,file_item):
        return file_item.get(OBJECT_FIELD, "") + " " + file_item.get("parameter", "") + " " + file_item.get(
            "action", "") + " " + str(file_item.get(PARTNER_ID))
