# -*- coding: utf-8 -*-
#上記、シェバングと呼ぶ？python3では指定しなくてもデフォルトでutf-8らしい。
#上記コメントアウトなのに意味あるの？
#main.py

import config
import robo_human_data
import decide_action_rulebase
import decide_action_TATsys
import exe_robo_action
import recog_utterance
import libokao
import random
import concurrent.futures
import recog_okao

#ロボットアクションの実行と、人間のリアクションの取得
def execute_action_and_get_human_reaction(robot_action):    #関数宣言。
    ret = robo_human_data.RobotHumanData()   #インスタンスretを宣言RobotHumanDataモジュールの、robotHumanData型。
    exe_robo_action.execute_robot_action(robot_action)
    ret.setRobotComment(robot_action[0])
    ret.setRobotMotion(robot_action[1])
    ret.setRobotLed(robot_action[2])

    recognized_comment = recog_utterance.recognize_utterance()  #ひとまとまりのセリフを認識するまで戻らない関数という想定。
    ret.setHumanComment(recognized_comment)
    ret.setOkaoVisionData()#本当は、ロボットアクション後、2秒後くらいに実行したいが、sleepすると全体ループに影響してしまう。実現するためにはここも別スレッドか

    if 1 == config.DEBUG_PRINT:
        print("recognized comment = ")
        print(recognized_comment)
        tmp_human_comment = ret.getHumanComment()
        print("1 ret human_comment = ")
        print(tmp_human_comment)

    return ret

def decide_action(robot_human_series_data):

    print("decide_actionが呼べてます！！！")

    #ロボットコメント、首振り動作、LED点灯のそれぞれテーブルの通し番号
    robot_action = [0,0,0]#0,0,0は応答なし

    #SW_DIALOGUE_SYSでの切り替え
    if 0 == config.SW_DIALOGUE_SYS:
        robot_action = decide_action_rulebase.decide_action_rulebase(robot_human_series_data)
    elif 1 == config.SW_DIALOGUE_SYS:
        robot_action = decide_action_TATsys.decide_action_TATsys(robot_human_series_data)
    else:
        pass
    return robot_action

def main():
    robot_human_series_data = []
    robot_action = [0,0,0]

#    robot_action = [10001,0,0]  #ロボットコメント、首振り動作、LED点灯のそれぞれテーブルの通し番号
#    robot_action = [20001,0,0]  #ロボットコメント、首振り動作、LED点灯のそれぞれテーブルの通し番号

#    execute_action_and_get_human_reaction(robot_action)

    end_flag = False
    if 1 == config.DEBUG_PRINT: print(end_flag)

    try:
        while end_flag == False:    #end_flagの設定どうしようかな
#            if robot_action != "noaction":
            if robot_action != (0,0,0):
                if 1 == config.DEBUG_PRINT: print("end_flag != False")
                #ロボットと人間の一連のやり取りデータを取得する。
                robot_human_data_tmp = execute_action_and_get_human_reaction(robot_action)

                if 1 == config.DEBUG_PRINT:
                    tmp_human_comment = robot_human_data_tmp.getHumanComment()
                    print("human_comment = ")
                    print(tmp_human_comment)

                #上で取得したロボットと人間の一連のやり取りデータをrobot_human_series_dataに追加する。
                robot_human_series_data.insert(0,robot_human_data_tmp)
                #ロボットと人間の一連のやり取りデータの保存上限をNUMで設定しておき、それより多くなった場合は古いものから消していく。

                if 1 == config.DEBUG_PRINT:
                    print(len(robot_human_series_data))

                if len(robot_human_series_data) > config.RESERVE_NUM_ROBOT_HUMAN_DATA:
                    robot_human_series_data.pop()
                #上で取得した、ロボットと人間の一連のやり取りデータを引数にして、robot_actionを返り値にする。
                robot_action = decide_action(robot_human_series_data)
                if 1 == config.DEBUG_PRINT:
                    print("robot_action[0]")
                    print(robot_action[0])

                if 1 == config.DEBUG_MODE0: end_flag = True

        #ここで、end処理する。
        print("ここでend処理する")
    except KeyboardInterrupt:
        pass
        print("Interrupted")

if __name__ == '__main__':
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
#    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)#認識中のLED光らない

    executor.submit(recog_okao.recognize_okao)
    executor.submit(main)
