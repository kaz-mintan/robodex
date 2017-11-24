#robotHumanData.py
import config

from datetime import datetime
from datetime import date
import get_weather

class RobotHumanData:
	'''OkaoVision情報、ロボアクション、ロボコメント、人コメント'''

	def __init__(self):
		robot_comment = ""
		robot_motion = []
		robot_led = []
		human_comment = ""
		time_stamp = 0	#時間だけでなく、日時も含まれていることを確認しておく。
		day_of_week = 0 #1:月 2:火 3:水 4:木 5:金 6:土 7:日
		wheather = 0	#天気と数値との関連付けは、取得先の設定を参考にする。
		okao_list = 0	#human_idも含む、または、別でhuman_idを作る。
#OKAOのデータの取り込みどうしよう？

	def getRobotComment(self):	#getRobotComment()メソッド
		return self.robot_comment

	def getRobotMotion(self):
		return self.robot_motion

	def getRobotLed(self):
		return self.robot_led

	def getHumanComment(self):
		return self.human_comment

	def getTimeStamp(self):
		return self.time_stamp

	def getDayOfWeek(self):
		return self.day_of_week

	def getWheather(self):
		return self.wheather

	def setRobotComment(self,RComment):	#setRobotComment()メソッド
		self.robot_comment = RComment

	def setRobotMotion(self,RMotion):
		self.robot_motion = RMotion

	def setRobotLed(self,RLed):
		self.robot_led = RLed

	def setHumanComment(self,HComment):
		self.human_comment = HComment

	def setTimeStamp(self):
		self.time_stamp = datetime.now()
		if 1 == config.DEBUG_PRINT:print(self.time_stamp.strftime("%Y/%m/%d %H:%M:%S"))

	def setDayOfWeek(self):
		self.today = datetime.today()
		self.day_of_week = self.today.isoweekday()

	def setWheather(self):
		self.wheather =

	def getOkaoVisionList(self,OKAOlist):
		self.okao_list = OKAOlist
		return 0
