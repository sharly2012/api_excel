#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from util.writeexcel import WriteExcel
from util.logger import Logger

logger = Logger(logger='base_api').get_log()


def send_requests(s, test_data):
    case_id = test_data['Id']
    url = test_data["Url"]
    method = test_data["Method"]
    logger.info("*******Test Case ：-----  %s  ----**********" % case_id)
    logger.info("Request Method：%s, 请求url:%s" % (method, url))

    try:
        params = test_data["Parameters"]
    except Exception as e:
        params = None
        logger.info(e)
    # 请求头部headers
    try:
        headers = test_data["Header"]
        logger.info("Request Header：%s" % headers)
    except Exception as e:
        headers = None
        logger.info(e)
    # post请求body类型
    data_type = test_data["Type"]
    logger.info("Request Params：%s" % params)

    # post请求body内容
    try:
        body_data = eval(test_data["Body"])
    except Exception as e:
        body_data = {}
        logger.info(e)

    if data_type == "data":
        body = body_data
    elif data_type == "json":
        body = json.dumps(body_data)
    else:
        body = body_data
    if method == "post":
        logger.info("body type is：%s , body content：%s" % (data_type, body))

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
        logger.info("Page Info：%s" % r.content)
        response['Id'] = test_data['Id']
        response['rowNum'] = test_data['rowNum']
        response["StatusCode"] = str(r.status_code)
        response["text"] = r.content.decode("utf-8")
        response["Time"] = str(r.elapsed.total_seconds())
        if response["StatusCode"] != "200":
            response["Error"] = response["text"]
        else:
            response["Error"] = ""
            response["Msg"] = ""
        if test_data["CheckPoint"] in response["text"]:
            response["Result"] = "Pass"
            logger.info("Test Result:   %s---->%s" % (case_id, response["Result"]))
        else:
            response["Result"] = "Fail"
        return response
    except Exception as msg:
        response["Msg"] = msg
        return response


def write_result(result, filename):
    # Return row_nub
    row_nub = result['rowNum']
    logger.info(row_nub)
    # Write Result
    wt = WriteExcel(filename)
    wt.write(row_nub, 8, result['StatusCode'])  # 写入返回状态码statuscode,第8列
    wt.write(row_nub, 9, result['Time'])  # 耗时
    wt.write(row_nub, 10, result['Error'])  # 状态码非200时的返回信息
    wt.write(row_nub, 12, result['Result'])  # 测试结果 pass 还是fail
    wt.write(row_nub, 13, result['Msg'])  # 抛异常
