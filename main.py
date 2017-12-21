
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

#ロボットアクションの実行と、人間のリアクションの取得
def execute_action_and_get_human_reaction(robot_action):    #関数宣言。
    ret = robo_human_data.RobotHumanData()   #インスタンスretを宣言RobotHumanDataモジュールの、robotHumanData型。
#ここで、OKAOVision認識データをリストに記憶するスレッドを起動する。
    exe_robo_action.execute_robot_action(robot_action)
    #下記、要素ごとに代入しているが、これでいいのか？
    #また、ロボットコメントなどの実データを入れる意味はあるのか？
    ret.setRobotComment(robot_action[0])
    ret.setRobotMotion(robot_action[1])
    ret.setRobotLed(robot_action[2])
#utteranceは発声の意
    recognized_comment = recog_utterance.recognize_utterance()  #ひとまとまりのセリフを認識するまで戻らない関数という想定。
    ret.setHumanComment(recognized_comment)

    if 1 == config.DEBUG_PRINT:
        print("recognized comment = ")
        print(recognized_comment)
        tmp_human_comment = ret.getHumanComment()
        print("1 ret human_comment = ")
        print(tmp_human_comment)

#OKAOVision停止の方法どうするか
    #okao_list = StopOkaoVisionThread()    #OKAOVision停止の想定。
    #ret.setOkaoVisionList(okao_list)
#    ret.sethogehoge...
    return ret

def decide_action(robot_human_series_data):
#    print(type(robot_human_series_data[0]))

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
    robot_action = [10001,0,0]  #ロボットコメント、首振り動作、LED点灯のそれぞれテーブルの通し番号
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

#robot_human_series_dataを元に、robot_actionを決める。
#robot_actionは、予め外部にテーブルを用意して選択肢から選択する。
#選択肢の要素は、モータの駆動角度、駆動速度、LEDの光らせ方


#以下、メモ
#アクションを返す必要が無い時はfalseを返す。

#会話が一段落するまでOKAOデータは取り続け，一段落した段階でリストで送る．
#getCurrentの時のOKAOのスレッドを立ち上げて，
#喋った言葉を覚えておきたいのはどこか．どこで覚えておきたいか．

#getCurrentDataの返すべきデータのクラスPrev_infoの変数のなかにはOKAOvision用のlistが用意してない．
#適当に決める．
#executeactionとget_human_reactionを分けるのではなく，一つの関数にしてしまうのも有り．

#以下、メモ、情報古い？
#get currentの中で、okaoからデータとるスレッド
#okaoと認識

#observed_data
#execute_robot_action
#prev info名前変える

#ファイルの分割は、どういう単位ですれば良いのだろう？
#main内で、複数関数書いてよい？

#robot_action = (0,0,0)
#a = execute_action_and_get_human_reaction(robot_action)


#decide_action---確認用---
#h_comment = "良いけど疲れた。"
#tmp_robo_h_s_data = []
#tmp = robo_human_data.RobotHumanData()
#tmp.setHumanComment(h_comment)
#tmp_robo_h_s_data.append(tmp)
#ret = decide_action(tmp_robo_h_s_data)
#print (ret)

main()
