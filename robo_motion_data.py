#robo_motion_data.py
#csvファイルのテーブルを開いて、このクラスでデータを保持する？

class RobotMotionData:

	def __init__(self):
		robot_comment = ""
		robot_motion = 0

	def getRobotComment(self):	#getRobotComment()メソッド
		return self.robot_comment

	def getTimeStamp(self):
		return self.time_stamp

	def setRobtComment(self,RComment):	#setRobotComment()メソッド
		self.robot_comment = RComment

	def setHumanComment(self,HComment):
		self.human_comment = HComment
