#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from util.writeexcel import WriteExcel
from util.logger import Logger

logger = Logger('base_api').get_log()


def send_requests(s, testdata):
    """封装requests请求"""
    method = testdata["Method"]
    url = testdata["Url"]
    try:
        params = eval(testdata["Parameters"])
    except Exception as e:
        params = None
        logger.info(e)
    try:
        headers = eval(testdata["Header"])
        print("请求头部：%s" % headers)
    except Exception as e:
        headers = None
        logger.info(e)
    data_type = testdata["Type"]
    test_nub = testdata['Id']
    print("*******正在执行用例：-----  %s  ----**********" % test_nub)
    print("请求方式：%s, 请求url:%s" % (method, url))
    print("请求params：%s" % params)

    try:
        body_data = eval(testdata["Body"])
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
        print("post请求body类型为：%s , body内容为：%s" % (data_type, body))

    verify = False
    response = {}

    try:
        r = s.request(method=method,
                      url=url,
                      params=params,
                      headers=headers,
                      data=body,
                      verify=verify
                      )
        print("Page Info：%s" % r.content.decode("utf-8"))
        response['Id'] = testdata['Id']
        response['rowNum'] = testdata['rowNum']
        response["StatusCode"] = str(r.status_code)
        response["text"] = r.content.decode("utf-8")
        response["Time"] = str(r.elapsed.total_seconds())
        if response["StatusCode"] != "200":
            response["Error"] = response["text"]
        else:
            response["Error"] = ""
            response["Msg"] = ""
        if testdata["CheckPoint"] in response["text"]:
            response["Result"] = "pass"
            print("Test Result:   %s---->%s" % (test_nub, response["Result"]))
        else:
            response["Result"] = "fail"
        return response
    except Exception as msg:
        response["Msg"] = str(msg)
        return response


def write_result(result, filename="result.xlsx"):
    # return row_nub
    row_nub = result['rowNum']
    # write status code
    wt = WriteExcel(filename)
    wt.write(row_nub, 8, result['StatusCode'])
    wt.write(row_nub, 9, result['Time'])
    wt.write(row_nub, 10, result['Error'])
    wt.write(row_nub, 12, result['Result'])
    wt.write(row_nub, 13, result['Msg'])
