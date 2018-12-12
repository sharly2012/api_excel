#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
import ddt
import requests
from util.baseutil import BaseUtil
from util import base_api
from util import readexcel
from util import writeexcel
from util.logger import Logger

root_path = BaseUtil().get_root_path()
test_xlsx = root_path + "/case/api_test.xlsx"
report_xlsx = root_path + "/report/result.xlsx"

test_data = readexcel.ExcelUtil(test_xlsx).dict_data()

logger = Logger(logger="testapi").get_log()


@ddt.ddt
class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        writeexcel.copy_excel(test_xlsx, report_xlsx)

    def setUp(self):
        logger.info("One testcase test start ...")

    @ddt.data(*test_data)
    def test_api(self, data):
        res = base_api.send_requests(self.s, data)
        # checkpoint
        check = data["CheckPoint"]
        logger.info("checkpoint->：%s" % check)
        # return result
        res_text = res["text"]
        logger.info("result->：%s" % res_text)
        # Assert
        self.assertTrue(check in res_text)
        base_api.write_result(res, report_xlsx)

    def tearDown(self):
        logger.info("The testcase execute finish ...")

    @classmethod
    def tearDownClass(cls):
        logger.info("All of the case done")


if __name__ == "__main__":
    unittest.main()
