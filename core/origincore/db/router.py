# -*- coding:UTF-8 -*-
import os
from django.conf import settings


class MasterRouter(object):
    def __init__(self, db_table, db_name, write=True):
        super(MasterRouter, self).__init__()
        self.db_table = db_table
        self.db_name = db_name          # TODO ??
        self.write = write

    def db_for_read(self, model, **kwargs):
        if model._meta.db_table in self.db_table:
            return self.db_name
        return None

    def db_for_write(self, model, **kwargs):
        if model._meta.db_table in self.db_table and self.write:
            return self.db_name
        return None

    def allow_relation(self, obj1, obj2, **kwargs):
        if obj1._meta.db_table in self.db_table or obj2._meta.db_table in self.db_table:
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'default':
            return model._meta.db_table in self.db_table
        elif model._meta.db_table in self.db_table:
            return False
        return None
