#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
import os
import sys
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from util.baseutil import BaseUtil
from util.HTMLTestRunner import HTMLTestRunner


def create_suite():
    test_dir = BaseUtil().get_root_path() + '/case/'
    discover = unittest.defaultTestLoader.discover(
        start_dir=test_dir,
        pattern='test_*.py',
        top_level_dir=None
    )
    return discover


def report():
    if len(sys.argv) > 1:
        report_name = BaseUtil().get_root_path() + '/report/' + sys.argv[1] + '_result.html'
    else:
        now = time.strftime("%Y-%m-%d_%H_%M_%S_")
        report_name = BaseUtil().get_root_path() + '/report/' + now + 'result.html'
    return report_name


def run_case(all_case):
    fp = open(report(), "wb")
    runner = HTMLTestRunner(stream=fp,
                            verbosity=2,
                            title="测试报告",
                            description="用例执行情况",
                            retry=1)
    runner.run(all_case)
    fp.close()


if __name__ == "__main__":
    cases = create_suite()
    run_case(cases)
