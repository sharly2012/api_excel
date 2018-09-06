#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from util.writeexcel import WriteExcel
from util.logger import Logger

logger = Logger(logger='base_api').get_log()


def send_requests(s, test_data):
    """封装requests请求"""
    method = test_data["Method"]
    url = test_data["Url"]
    try:
        params = eval(test_data["Parameters"])
    except Exception as e:
        params = None
        logger.info(e)
    try:
        headers = eval(test_data["Header"])
        print("请求头部：%s" % headers)
    except Exception as e:
        headers = None
        logger.info(e)
    # post请求body类型
    data_type = test_data["Type"]

    test_nub = test_data['Id']
    print("*******正在执行用例：-----  %s  ----**********" % test_nub)
    print("请求方式：%s, 请求url:%s" % (method, url))
    print("请求params：%s" % params)

    try:
        body_data = eval(test_data["Body"])
    except Exception as e:
        body_data = {}
        logger.info(e)
    # 判断传data数据还是json
    if data_type == "data":
        body = body_data
    elif data_type == "json":
        body = json.dumps(body_data)
    else:
        body = body_data
    if method == "post":
        print("post请求body类型为：%s ,body内容为：%s" % (data_type, body))

    verify = False
    res = {}

    try:
        r = s.request(method=method,
                      url=url,
                      params=params,
                      headers=headers,
                      data=body,
                      verify=verify
                      )
        print("Page Info：%s" % r.content)
        res['id'] = test_data['Id']
        res['rowNum'] = test_data['rowNum']
        res["StatusCode"] = str(r.status_code)
        res["text"] = r.content
        res["Time"] = str(r.elapsed.total_seconds())
        if res["StatusCode"] != "200":
            res["Error"] = res["text"]
        else:
            res["Error"] = ""
        res["Msg"] = ""
        if test_data["CheckPoint"] in res["text"]:
            res["Result"] = "pass"
            print("Test Result:   %s---->%s" % (test_nub, res["Result"]))
        else:
            res["Result"] = "fail"
        return res
    except Exception as msg:
        res["Msg"] = str(msg)
        return res


def write_result(result, filename="result.xlsx"):
    # Return row_nub
    row_nub = result['rowNum']
    # Write Result
    wt = WriteExcel(filename)
    wt.write(row_nub, 8, result['StatusCode'])
    wt.write(row_nub, 9, result['Time'])
    wt.write(row_nub, 10, result['Error'])
    wt.write(row_nub, 12, result['Result'])
    wt.write(row_nub, 13, result['Msg'])
