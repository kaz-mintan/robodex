# -*- coding: utf-8 -*-
#上記、シェバングと呼ぶ？python3では指定しなくてもデフォルトでutf-8らしい。
#上記コメントアウトなのに意味あるの？
#main.py

import config
import robo_human_data
import decide_action_rulebase
import decide_action_TATsys
import exe_robo_action
# recog_utterance（無料api、リクエスト上限あり）と、recog_utterance_gcspeechapi（有料api）を切り替える
import recog_utterance_gcspeechapi as recog_utterance
import libokao
import random
import recog_okao

import multi_exe_ctrl
import time

import recog_utterance_gcspeechapi

def set_okao_vision_data(ret):
    config.debug_print("set_okao_vision_data関数の中1")
    time.sleep(2)
    config.debug_print("set_okao_vision_data関数の中2")
    ret.setOkaoVisionData(recog_okao.okao_data)
    config.debug_print("set_okao_vision_data関数の中3")

#ロボットアクションの実行と、人間のリアクションの取得
def execute_action_and_get_human_reaction(robot_action):
    ret = robo_human_data.RobotHumanData()  # インスタンスretを宣言RobotHumanDataモジュールの、robotHumanData型。
    if robot_action[3] == 0:
        recog_utterance_gcspeechapi.recognizing_utterance_flag = 1
    else:
        pass
    exe_robo_action.execute_robot_action(robot_action)
    ret.setRobotComment(robot_action[0])
    ret.setRobotMotion(robot_action[1])
    ret.setRobotLed(robot_action[2])
    ret.setRecgCmntSkipFlag(robot_action[3])

    if robot_action[3] == 0:
        recognized_comment = recog_utterance_gcspeechapi.recognize_utterance()  #ひとまとまりのセリフを認識するまで戻らない関数という想定。
    else:
        recognized_comment = ""

    ret.setHumanComment(recognized_comment)
#    ret.setOkaoVisionData()#本当は、ロボットアクション後、2秒後くらいに実行したいが、sleepすると全体ループに影響してしまう。実現するためにはここも別スレッドか

#   下の、マルチ実行にすると、動作しない。
#    config.debug_print("set_okao_vision_data関数を呼ぶ前")
    multi_exe_ctrl.executor.submit(set_okao_vision_data,ret)
#    config.debug_print("set_okao_vision_data関数を呼んだ後")

    config.debug_print("recognized comment = " +str(recognized_comment))
    config.debug_print("ret.getHumanComment() = " +str(ret.getHumanComment()))

    return ret

def decide_action(robot_human_series_data):

    config.debug_print("decide_actionが呼べてます！！！")

    #ロボットコメント、首振り動作、LED点灯のそれぞれテーブルの通し番号
    robot_action = [0,0,0,0]#0,0,0,0は応答なし、認識実行あり

    #SW_DIALOGUE_SYSでの切り替え
    if 0 == config.SW_DIALOGUE_SYS:
        robot_action = decide_action_rulebase.decide_action_rulebase(robot_human_series_data)
    elif 1 == config.SW_DIALOGUE_SYS:
        robot_action = decide_action_TATsys.decide_action_TATsys(robot_human_series_data)
    else:
        pass

    config.debug_print("decide_action関数内robot_acton:" +str(robot_action))

    return robot_action

def main():
    multi_exe_ctrl.executor.submit(recog_okao.recognize_okao)

    robot_human_series_data = []
    robot_action = [0,0,0,0]

    end_flag = False
    if 1 == config.DEBUG_PRINT: print(end_flag)

    try:
        while end_flag == False:    #end_flagの設定どうしようかな
            print("while内robot_action:",robot_action)
            if robot_action != (0,0,0,0):
                config.debug_print("end_flag != False")
                #ロボットと人間の一連のやり取りデータを取得する。
                config.debug_print("mainの中で、execute_action_and_get_human_reaction関数開始")
                robot_human_data_tmp = execute_action_and_get_human_reaction(robot_action)
                config.debug_print("mainの中で、execute_action_and_get_human_reaction関数終了")
                config.debug_print("robot_human_data_tmp.getHumanComment():" +str(robot_human_data_tmp.getHumanComment()))

                #上で取得したロボットと人間の一連のやり取りデータをrobot_human_series_dataに追加する。
                robot_human_series_data.insert(0,robot_human_data_tmp)
                config.debug_print("len(robot_human_series_data)" +str(len(robot_human_series_data)))

                #ロボットと人間の一連のやり取りデータの保存上限をRESERVE_NUM_ROBOT_HUMAN_DATAで設定しておき、それより多くなった場合は古いものから消していく。
                if len(robot_human_series_data) > config.RESERVE_NUM_ROBOT_HUMAN_DATA:
                    robot_human_series_data.pop()
                #上で取得した、ロボットと人間の一連のやり取りデータを引数にして、robot_actionを返り値にする。
                robot_action = decide_action(robot_human_series_data)
                config.debug_print("mainの中で、decide_action関数終了")
                config.debug_print("robot_action: " +str(robot_action))

                if 1 == config.DEBUG_MODE0: end_flag = True

        #ここで、end処理する。
    except KeyboardInterrupt:
        pass
        print("Interrupted")

if __name__ == '__main__':
    main()
