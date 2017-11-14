#coding: UTF-8
#decide_action_rulebase.py
#関数よりクラスの方が良いのかな？

import tbl_human_comment
import tbl_robo_comment

def pic_human_term(human_comment):

pic_term_list = []
    human_comment = "良いけど疲れた。"

    for key in dict_human_term:

        list = dict_human_term[key]

        for number in range(len(list)):
#            print (list[number])
            if human_comment.find(list[number]) > -1:
#               if True == list[number] in human_comment:　これだとうまくいかない
#                print(msg.find(list[number]))
                pic_term_list.append(key)
                break
            else:
                pass

            for number in range(len(pic_term_list)):
                print (pic_term_list[number])

    return pic_term_list


def dialogue_algorithm_rulebase(pic_human_term):
#tbl_robo_commentの中を参照して、robot_commentを返す。
#ルールを追加・確認する際に、ファイルを参照しないといけないのは煩わしいので、今後改善したい。
#tbl_robo_commentの中で記載しているlistを辞書型にすれば、意味のあるkeyを持たせる事ができるが、
#他のファイルでは、通し番号で管理しているので、併用が難しい。

    if (True == "良い" in pic_human_term) and (True == "疲れた" in pic_human_term):
        robot_comment = 4
    return robot_comment


def decide_action_rulebase(robot_human_series_data)

    robot_action = [0,0,0]#ロボットのコメント、モーション、LEDの、それぞれのテーブルのID

    #rulebaseシステムでhogehogeする
    robot_human_data_newest = robot_human_series_data[0]
    tmp_human_comment = robot_human_data_newest.getHumanComment()

    pic_term_list = pic_human_term(tmp_human_comment)

    robot_comment = dialogue_algorithm_rulebase(pic_term_list)

    robot_action = [robot_comment,0,0]

#コメント表、アクション表からどう取得するかを考える必要あり。

    return robot_action
