#robotHumanData.py

from datetime import datetime

class RobotHumanData:
	'''OkaoVision情報、ロボアクション、ロボコメント、人コメント'''

	def __init__(self):
		robot_comment = ""
		robot_motion = 0
		human_comment = ""
		time_stamp = 0
		okao_list = 0
#OKAOのデータの取り込みどうしよう？

	def getRobotComment(self):	#getRobotComment()メソッド
		return self.robot_comment

	def getRobotMotion(self):
		return self.robot_motion

	def getHumanComment(self):
		return self.human_comment

	def getTimeStamp(self):
		return self.time_stamp

	def setRobtComment(self,RComment):	#setRobotComment()メソッド
		self.robot_comment = RComment

	def setRobotMotion(self,RMotion):
		self.robot_motion = Motion

	def setHumanComment(self,HComment):
		self.human_comment = HComment

	def setTimeStamp(self):
		self.time_stamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

	def getOkaoVisionList(self,OKAOlist):
		self.okao_list = OKAOlist
		return 0
