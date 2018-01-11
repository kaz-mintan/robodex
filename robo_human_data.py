# -*- coding: utf-8 -*-
#robotHumanData.py
import config

from datetime import datetime
from datetime import date
import get_weather
#import recog_okao

class RobotHumanData:
	'''OkaoVision情報、ロボアクション、ロボコメント、人コメント'''

	def __init__(self):
		self.robot_comment = ""
		self.robot_motion = []#中身を入れた方がいいのか？
		self.robot_led = []#中身を入れた方がいいのか？
		self.recog_commnet_skip_flag = 0
		self.human_comment = ""
		self.time_stamp = 0	#時間だけでなく、日時も含まれていることを確認しておく。
		self.day_of_week = 0 #1:月 2:火 3:水 4:木 5:金 6:土 7:日
		self.wheather_data = {}
		self.wheather_today = [0,0,0,0]#天気と数値との関連付けは、取得先の設定を参考にする。
		self.okao_data = [[]]	#human_idも含む、または、別でhuman_idを作る。idは今回は作れず。

#OKAOのデータの取り込みどうしよう？

	def getRobotComment(self):	#getRobotComment()メソッド
		return self.robot_comment

	def getRobotMotion(self):
		return self.robot_motion

	def getRobotLed(self):
		return self.robot_led

	def getRecgCmntSkipFlag(self):
		return self.recog_commnet_skip_flag

	def getHumanComment(self):
		return self.human_comment

	def getTimeStamp(self):
		return self.time_stamp

	def getDayOfWeek(self):
		return self.day_of_week

	def getWheather(self):
		return self.wheather_data

	def getWheatherSimpleToday(self):
		return self.wheather_today

	def getOkaoVisionData(self):
		print("getOkaoVisionData: ",self.okao_data)
		return self.okao_data

	def setRobotComment(self,RComment):	#setRobotComment()メソッド
		self.robot_comment = RComment

	def setRobotMotion(self,RMotion):
		self.robot_motion = RMotion

	def setRobotLed(self,RLed):
		self.robot_led = RLed

	def setRecgCmntSkipFlag(self,Frecogcomn):
		self.recog_commnet_skip_flag = Frecogcomn

	def setHumanComment(self,HComment):
		self.human_comment = HComment

	def setTimeStamp(self):
		self.time_stamp = datetime.now()
		if 1 == config.DEBUG_PRINT:print(self.time_stamp.strftime("%Y/%m/%d %H:%M:%S"))

	def setDayOfWeek(self):
		self.today = datetime.today()
		self.day_of_week = self.today.isoweekday()

	def setWheather(self):
		self.weather_data = get_weather.get_weather()
		self.today_weather_term = self.weather_data['forecasts'][0]['telop']#今日の天気

		if "晴" in self.today_weather_term:
			self.weather_today[0] = 1
		if "曇" in self.today_weather_term:
			self.weather_today[1] = 1
		if "雨" in self.today_weather_term:
			self.weather_today[2] = 1
		if "雪" in self.today_weather_term:
			self.weather_today[3] = 1

#		print(self.today_weather_term)
#		print(self.weather_today)

	def setOkaoVisionData(self, okao):
		self.okao_data = okao
		print("debug/setOkaoVisionData: ",self.okao_data)
		return self.okao_data
