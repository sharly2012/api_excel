#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymysql
from util.baseutil import BaseUtil
from util.logger import Logger

logger = Logger(logger="MysqlDB").get_log()

db_host = BaseUtil().get_config_value("MySql", "host")
port = BaseUtil().get_config_value("MySql", "port")
username = BaseUtil().get_config_value("MySql", "username")
password = BaseUtil().get_config_value("MySql", "password")
db_name = BaseUtil().get_config_value("MySql", "db_name")
charset = BaseUtil().get_config_value("MySql", "charset")


class MysqlDB:

    def __init__(self):
        try:
            self.connection = pymysql.connect(host=db_host,
                                              port=int(port),
                                              user=username,
                                              password=password,
                                              database=db_name,
                                              charset=charset)
        except pymysql.err.OperationalError as e:
            logger.info("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def execute_sql(self, sql_querry):
        con = self.connection
        cursor = con.cursor()
        cursor.execute(sql_querry)
        querry_result = cursor.fetchall()
        return querry_result


if __name__ == '__main__':
    aaa = "SELECT * FROM om_admin LIMIT 10"
    db = MysqlDB()
    rows = db.execute_sql(aaa)
    for row in rows:
        uid = row[0]
        name = row[1]
        print(uid, name)
