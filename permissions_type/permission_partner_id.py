from abc import ABC
from collections import defaultdict

from permissions_type.permission import Permission

SELECT_QUERY = r"""select partner_id as partnerid, type, name as permissions 
from permission where partner_id = %s """

TYPE = "type"
NAME = "name"
PARTNER_ID = "partnerid"
OBJECT_FIELD = "object"
SERVICE_FIELD = "service"


class PermissionPartnerId(Permission):
    def convert_file_to_dict(self, file):
        pass

    def convert_db_to_dict(self, db_dict):
        pass

    def print_item(self, item):
        string_to_print = ""
        if item.get(PARTNER_ID) is not None: string_to_print += '\033[97m' + PARTNER_ID + ": " + '\033[95m' + str(
            item.get(PARTNER_ID)) + ", "
        if item.get("type") is not None: string_to_print += '\033[97m' + "type: " + '\033[95m' + str(
            item.get("type"))
        return string_to_print + '\033[0m'

    def get_permission_from_db(self, my_db, object_name):
        query = SELECT_QUERY % object_name
        permission_item_list = super().get_permission_from_db(my_db, query)
        db_permissions_dict = self.get_permission_item(permission_item_list)
        return db_permissions_dict

    def get_permission_item(self, permission_item_list):
        db_permissions_dict = defaultdict(dict)
        for item in permission_item_list:
            key = str(item.get("partnerid")) + "_" + str(item.get("type"))
            if db_permissions_dict[key]:
                db_permissions_dict[key]["permissions"].append(item.get("permissions"))
            else:
                item["permissions"] = [item.get("permissions")]
                db_permissions_dict[key] = item
        return db_permissions_dict

    def get_file_permissions_dict(self, section, config):
        file_permissions_dict, objects = super().get_file_permissions_dict(section, config, PARTNER_ID)
        partner_dict = defaultdict(dict)
        {self.create_partner_dict(x, partner_dict) for x in file_permissions_dict.values()}
        return partner_dict, set(objects)

    def create_partner_dict(self, file_permission, partner_dict):
        key = file_permission.get(PARTNER_ID) + "_" + file_permission.get(TYPE)
        partner_dict[key][PARTNER_ID] = file_permission.get(PARTNER_ID)
        partner_dict[key][TYPE] = file_permission.get(TYPE)
        partner_dict[key][NAME] = file_permission.get(NAME) if partner_dict[key].get(NAME) is None \
            else partner_dict[key][NAME] + "," + file_permission.get(NAME)

    def str_item(self,file_item):
        return str(file_item.get(PARTNER_ID)) + " " + str(file_item.get("type", ""))