# -*- coding: utf-8 -*-
# create by Aramis
from module_mysql import MysqlClient


class MgController:

    def __init__(self):
        self.client = MysqlClient()

    def check_version(self, version_code, version_name):
        pass
