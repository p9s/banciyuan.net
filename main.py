#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ********************************************************************
# Copyright © 2022 p9s
# File Name: main.py
# Author: p9s
# Email: mc.cheung@aol.com
# Created: 2022-09-06 19:49:32 (CST)
# Last Update: TUESDAY 2022-09-06 21:01:16 (CST)
#          By:
# Description:
# ********************************************************************
import requests
import urllib.parse
import re
import xlsxwriter

# urlencode
key = "绘师"
params = {
    'k': urllib.parse.quote(key)
}

url = 'https://bcy.net/search/user'

headers = {
    'authority': 'bcy.net',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,fr;q=0.6,it;q=0.5',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://bcy.net/search/home?k=' + params['k'],
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
}


res = requests.get(url, headers=headers, params=params)
re_res = re.findall(r"\\\"userSearchId\\\":\\\"(.*?)\\\"", res.text)

book = xlsxwriter.Workbook("users.xlsx")
sheet = book.add_worksheet()

sheet.write(0, 0, "ID")
sheet.write(0, 1, "Nick")
sheet.write(0, 2, "intro")
sheet.write(0, 3, "follower")
sheet.write(0, 4, "following")
sheet.write(0, 5, "gender")
sheet.write(0, 6, "tags")

row = 1


if re_res:
    print(re_res)
    search_id = re_res[0]

    gp = {}
    gp['searchId'] = search_id
    gp['size'] = 30
    gp['query'] = key

    get_user_header = {
        'authority': 'bcy.net',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,fr;q=0.6,it;q=0.5',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://bcy.net/search/user?k=%E7%BB%98%E5%B8%88',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }


    while True:
        gp['from'] = int(gp.get('from', 0)) + 1
        print("current page: " + str(gp['from']))


        j = requests.get('https://bcy.net/apiv3/search/getUser', headers=get_user_header, params=gp).json()

        if 'user_list' in j:
            for _dt in j['user_list']:
                sheet.write(row, 0, _dt['uid'])
                sheet.write(row, 1, _dt['uname'])
                sheet.write(row, 2, _dt['self_intro'])
                sheet.write(row, 3, _dt['follower'])
                sheet.write(row, 4, _dt['following'])
                sheet.write(row, 5, '女' if int(_dt['sex']) == 0 else '男')

                tags = ""
                for tag in _dt['utags']:
                    tags += tag['ut_name']
                sheet.write(row, 6, tags)

                row += 1

        if gp['from'] == 8:
            break

    book.close()

else:
    print("find search id fail")
