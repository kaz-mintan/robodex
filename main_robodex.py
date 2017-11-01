#main_robodex.py

import prev_info
import robo_response_rulebase

#mainの書き方
#main関数を実行する形でデバッグする
#tryに内包する


#prev_info = get_prev_info.Get_prev_info()	#prev_infoは、Get_prev_info型のインスタンス
#print(prev_info.prev_robo_comment)
#print(prev_info.prev_robo_action)
#print(prev_info.prev_human_comment)
#print(prev_info.get_okao_info())
#print(prev_info.prev_time_stamp)

#next_robo_response = robo_response_rulebase.Get_robo_response_rulebase()
#print(next_robo_response.next_robo_comment)
#print(next_robo_response.next_robo_action)

prev_info0 = prev_info.Prev_info()
prev_info0.setPrevRoboComment("ロボはこう言いました。")
print(prev_info0.getPrevRoboComment())

#prev_info = get_prev_info.Get_prev_info()	#prev_infoは、Get_prev_info型のインスタンス
#print(prev_info.prev_robo_comment)
#print(prev_info.prev_robo_action)
#print(prev_info.prev_human_comment)
#print(prev_info.get_okao_info())
#print(prev_info.prev_time_stamp)

#next_robo_response = robo_response_rulebase.Get_robo_response_rulebase()
#print(next_robo_response.next_robo_comment)
#print(next_robo_response.next_robo_action)


