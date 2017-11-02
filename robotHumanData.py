#get_prev_info.py

from datetime import datetime

#ここで、どうデータを取得するか（どうデータを格納するか）を考える必要がある。（肝）

#class Get_prev_info:
#	prev_robo_comment = "ロボはこう言いました。"
#	prev_robo_action = 0
#	prev_human_comment = "人はこう言いました。"
#	def get_okao_info(self):
#		return 0
#	prev_time_stamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")


class Prev_info:
	'''OkaoVision情報、ロボアクション、ロボコメント、人コメント'''

	def __init__(self):
		prev_robo_comment = ""
		prev_robo_action = 0
		prev_human_comment = ""
		prev_time_stamp = 0

#Okaoのデータの取り込みどうしよう？

	def getPrevRoboComment(self):	#getPrevRoboComment()メソッド
		return self.prev_robo_comment

	def getPrevRoboAction(self):
		return self.prev_robo_action

	def getPrevHumanComment(self):
		return self.prev_human_comment

	def getPrevTimeStamp(self):
		return self.prev_time_stamp

	def setPrevRoboComment(self,RComment):	#setPrevRoboComment()メソッド
		self.prev_robo_comment = RComment

	def setPrevRoboAction(self,RAction):
		self.prev_robo_action = RAction

	def setPrevHumanComment(self,HComment):
		self.prev_human_comment = HComment

	def setPrevTimeStamp(self):
		self.prev_time_stamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")


	def get_okao_info(self):
		return 0


