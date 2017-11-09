# -*- coding: utf-8 -*-
#上記、シェバングと呼ぶ？python3では指定しなくてもデフォルトでutf-8らしい。
#上記コメントアウトなのに意味あるの？
#main.py

import robo_human_data
import robot_action_rulebase
import exe_robo_action

#ロボットアクションの実行と、人間のリアクションの取得
def execute_action_and_get_human_reaction(robot_action):    #関数宣言。
    ret = robotHumanData.RobotHumanData()   #インスタンスretを宣言RobotHumanDataモジュールの、robotHumanData型。
#    ここで、OKAOVision認識データをリストに記憶するスレッドを起動する。
    execute_robot_action(robot_action)
    ret.setRobotAction(robot_action)
#utteranceは発声の意
    recognized_comment = recognize_utterance()  #ひとまとまりのセリフを認識するまで戻らない関数という想定。
    ret.setHumanComment(recognized_comment)
#OKAOVision停止の方法どうするか
    okao_list = StopOkaoVisionThread()    #OKAOVision停止の想定。
    ret.setOkaoVisionList(okao_list)
    ret.sethogehoge...
    return ret

#robotHumanData.pyでモジュールを用意する必要あり。RobotHumanDataクラス
#    ret.setRobotAction(robot_action)
#    ret.setOkaoVisionList(okao_list)
#    ret.sethogehoge...

#execute_robot_action(robot_action)関数を用意する必要あり

#recognize_utterance()関数（返り値あり）を用意する必要あり
#認識したコメントを返す




def main_robodex():

    #最大で保存しておく、ロボットと人間の一連のやり取りデータの数
    RESERVE_NUM_ROBOT_HUMAN_DATA = 10

    #対話システムの選択スイッチ、まずは手動切り替えにする。
    #0:ルールベースシステム　1:TAT学習システム
    SW_DIALOGUE_SYS = 0

    robot_human_series_data = []
    #...
    try:
        while end_flag == False:    #end_flagの設定どこでやるの？
            if robot_action != "noaction":
                #ロボットと人間の一連のやり取りデータを取得する。
                robot_human_data_tmp = execute_action_and_get_human_reaction(robot_action)
                #上で取得したロボットと人間の一連のやり取りデータをdata_listに追加する。
                robot_human_series_data.append(robot_human_data_tmp)
                #ロボットと人間の一連のやり取りデータの保存上限をNUMで設定しておき、それより多くなった場合は古いものから消していく。
                if len(robot_human_series_data) > RESERVE_NUM_ROBOT_HUMAN_DATA:
                robot_human_series_data.popleft()
                #上で取得した、ロボットと人間の一連のやり取りデータを引数にして、robot_actionを返り値にする。
                robot_action = decide_action(SW_DIALOGUE_SYS, robot_human_series_data)

    except KeyboardInterrupt:
        pass
        print("Interrupted")

#robot_action関数を用意しておく必要あり。
#data_listを元に、robot_actionを決める。
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
