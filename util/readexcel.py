#!/usr/bin/python3
# -*- coding: utf-8 -*-
import xlrd
from util.logger import Logger

logger = Logger(logger='BasePage').get_log()


class ExcelUtil():
    def __init__(self, excel_path, sheet_name="Sheet1"):
        self.data = xlrd.open_workbook(excel_path)
        self.table = self.data.sheet_by_name(sheet_name)
        # 获取第一行作为key值
        self.keys = self.table.row_values(0)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols

    def dict_data(self):
        if self.rowNum <= 1:
            logger.info("总行数小于1")
        else:
            r = []
            j = 1
            for i in list(range(self.rowNum - 1)):
                s = dict()
                s['rowNum'] = i + 2
                values = self.table.row_values(j)
                for x in list(range(self.colNum)):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j += 1
            return r
