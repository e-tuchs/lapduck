#! -*- coding: utf-8 -*-
import logging
from bson.son import SON
from functools import wraps
from pymongo.cursor import Cursor
from pymongo import ReplicaSetConnection, ReadPreference, Connection
from pymongo import DESCENDING, ASCENDING

logger = logging.getLogger('origincore')


class MongodbStorage(object):
    _db = None
    ORDER_DESC = DESCENDING
    ORDER_ASC = ASCENDING

    def __init__(self, conn_str, db_name):
        try:
            if conn_str.find("rs") == -1:
                _conn = Connection(conn_str,max_pool_size=300,safe=True,
                    read_preference=ReadPreference.SECONDARY_ONLY)
            else:
                _conn = ReplicaSetConnection(conn_str,max_pool_size=300,safe=True,
                    read_preference=ReadPreference.SECONDARY_ONLY)
            self._db = _conn[db_name]
            self._conn = _conn
        except Exception, e:
            logger.exception('Connect to mongodb server error: %s', e)
            raise e

