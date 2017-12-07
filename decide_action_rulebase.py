#coding: UTF-8
#decide_action_rulebase.py
#関数よりクラスの方が良いのかな？

import tbl_human_comment
import tbl_robo_comment
import config

import robo_human_data
import random

def pic_human_term(human_comment):

#    human_comment = "あいうえお"

    pic_term_list = []
    if 1 == config.DEBUG_PRINT: print(human_comment)

    #dict_human_termは、一旦取り込んだ方がいいか？
    for key in tbl_human_comment.dict_human_term:

        list = tbl_human_comment.dict_human_term[key]

        for number in range(len(list)):
#            print (list[number])
            if human_comment.find(list[number]) > -1:
#               if True == list[number] in human_comment:　これだとうまくいかない
#               print(msg.find(list[number]))
                pic_term_list.append(key)
                break
            else:
                pass

    if (1 == config.DEBUG_PRINT):
        for number in range(len(pic_term_list)):
            print ("pic_human_term関数内のpic_term_list" + pic_term_list[number])

    return pic_term_list


def dialogue_algorithm_rulebase(pic_human_term):
#tbl_robo_commentの中を参照して、robot_commentを返す。
#ルールを追加・確認する際に、ファイルを参照しないといけないのは煩わしいので、今後改善したい。
#tbl_robo_commentの中で記載しているlistを辞書型にすれば、意味のあるkeyを持たせる事ができるが、
#他のファイルでは、通し番号で管理しているので、併用が難しい。

    if (1 == config.DEBUG_PRINT):
        print(pic_human_term)

    robot_comment_no = 0

    if  (True == ("良い" in pic_human_term)) and (True == ("疲れた" in pic_human_term)):
        robot_comment_no = 4
    elif(True == ("こんにちは" in pic_human_term)):
        robot_comment_no = random.choice([6,10,11,12,13,14,15,1003,1004,1010,1011])
    elif(True == ("お疲れ様" in pic_human_term)):
        robot_comment_no = random.choice([19,20,21,1005,1006,1007])
    elif(True == ("私は" in pic_human_term)) and (True == ("と言います" in pic_human_term)):
        robot_comment_no = 7
    elif(True == ("年齢" in pic_human_term)) and (True == ("当て" in pic_human_term)):
        robot_comment_no = 8
    elif(True == ("今日" in pic_human_term)) and (True == ("天気" in pic_human_term)):
        robot_comment_no = 50

    else:
        pass

    return robot_comment_no


def decide_action_rulebase(robot_human_series_data):

    robot_action = [0,0,0]#ロボットのコメント、モーション、LEDの、それぞれのテーブルのID

#    robot_human_data_newest = robo_human_data.RobotHumanData()

    robot_human_data_newest = robot_human_series_data[0]
    tmp_human_comment = robot_human_data_newest.getHumanComment()

    pic_term_list = pic_human_term(tmp_human_comment)

    robot_comment_no = dialogue_algorithm_rulebase(pic_term_list)

    robot_action = [robot_comment_no,0,0]

#コメント表、アクション表からどう取得するかを考える必要あり。

    return robot_action

#以下、関数別debug用

#---dialogue_algorithm_rulebase確認用---
#tmp_term = "良いけど疲れた"
#print(dialogue_algorithm_rulebase(tmp_term))

#---pic_human_term確認用---
#h_comment = "良いけど疲れた。"
#print(pic_human_term(h_comment))

#---decide_action_rulebase確認用---
#h_comment = "良いけど疲れた。"
#tmp_robo_h_s_data = []
#tmp = robo_human_data.RobotHumanData()
#tmp.setHumanComment(h_comment)
#tmp_robo_h_s_data.append(tmp)
#ret = decide_action_rulebase(tmp_robo_h_s_data)
#print (ret)
