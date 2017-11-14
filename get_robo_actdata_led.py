

#csvファイルのテーブルを開いて、通し番号に対応するデータを持ってくる
class GetRobotActionDataOfLed:

        def __init__(self):
                robot_action_data_of_Led = (0,0,0,0,0,0,0,0,0,0)

        def getRobotLed(self,led_tbl_no):
		#ここで、csvなどのテーブルファイルを開き、led_tbl_noに対応するコメントを返り値の変数に入れる

                return self.robot_action_data_of_led
