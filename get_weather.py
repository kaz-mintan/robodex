#!/usr/bin/env python
# coding: utf-8

import requests
import json
import config

def get_weather():

	today_wheather = [0,0,0,0]#"晴"、"曇"、"雨"、"雪"という単語がそれぞれが含まれる場合は1を立てる。

	url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
#	payload = {'city': '280010'} # Kobe
	payload = {'city': '130010'} # Tokyo
	data = requests.get(url, params = payload).json()

	if 1 == config.DEBUG_PRINT:
		print(data)
		print(data['title'])
		for weather in data['forecasts']:
			print(weather['dateLabel'] + ':' + weather['telop'])
		print (type(data))

	return data

#get_weather()

#	today_wheather_term = tmp['forecasts'][0]['telop']#今日の天気
#
#	if "晴" in today_wheather_term:
#		today_wheather[0] = 1
#	if "曇" in today_wheather_term:
#		today_wheather[1] = 1
#	if "雨" in today_wheather_term:
#		today_wheather[2] = 1
#	if "雪" in today_wheather_term:
#		today_wheather[3] = 1
#
#	return today_wheather


#晴、曇、雨、雪
#が含まれるかどうかで、[]配列内0,1を4つ用意する

#ライブドア天気の天気アイコンの凡例より
#晴				晴れ時々曇り		晴れ時々雨
#晴れ時々雪		晴れのち曇り		晴れのち雨
#晴れのち雪		曇り				曇り時々晴れ
#曇り時々雨		曇り時々雪			曇りのち晴れ
#曇りのち雨		曇りのち雪			雨
#雨時々晴れ		雨時々止む(曇り)		雨時々雪
#雨のち晴れ		雨のち曇り			雨のち雪
#雨で暴風を伴う	雪				雪時々晴れ
#雪時々止む(曇り)	雪時々雨		雪のち晴れ
#雪のち曇り		雪のち雨		暴風雪
