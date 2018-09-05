#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
import ddt
import os
import requests
from util.baseutil import BaseUtil
from util import base_api
from util import readexcel
from util import writeexcel

root_path = BaseUtil().get_root_path()
test_xlsx = root_path + "/case/api_test.xlsx"
report_xlsx = root_path + "/report/result.xlsx"

test_data = readexcel.ExcelUtil(test_xlsx).dict_data()


@ddt.ddt
class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        writeexcel.copy_excel(test_xlsx, report_xlsx)

    def setUp(self):
        pass

    @ddt.data(*test_data)
    def test_api(self, data):
        res = base_api.send_requests(self.s, data)

        base_api.write_result(res, filename=report_xlsx)
        # checkpoint
        check = data["CheckPoint"]
        print("checkpoint->：%s" % check)
        # return result
        res_text = res["text"]
        print("result->：%s" % res_text)
        # Assert
        self.assertTrue(check in res_text)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
