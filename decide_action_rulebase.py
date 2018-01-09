##coding: UTF-8

#decide_action_rulebase.py
#関数よりクラスの方が良いのかな？

import tbl_human_comment
import tbl_robo_comment
import config

import robo_human_data
import random

def pic_human_term(human_comment):
    pic_term_list = []
    config.debug_print("human_comment: "+human_comment)

    #dict_human_termは、一旦取り込んだ方がいいか？
    for key in tbl_human_comment.dict_human_term:
        list = tbl_human_comment.dict_human_term[key]
        for number in range(len(list)):
            if human_comment.find(list[number]) > -1:
#               if True == list[number] in human_comment:　これだとうまくいかない
#               print(msg.find(list[number]))
                pic_term_list.append(key)
                break
            else:
                pass

    for number in range(len(pic_term_list)):
        config.debug_print("pic_human_term関数内のpic_term_list" + pic_term_list[number])

    return pic_term_list


def dialogue_algorithm_rulebase(robot_human_series_data):
#tbl_robo_commentの中を参照して、robot_commentを返す。
    config.debug_print("dialogue_algorithm_rulebaseが呼べてます。")

    values = robot_human_series_data[:config.RESERVE_NUM_ROBOT_HUMAN_DATA]#下の書き方でも良いが、robot_human_series_dataの大きさがRESERVE_NUM_ROBOT_HUMAN_DATAより大きくなってしまった時（バグ）の保険のため
#    values = series_data

    n = config.RESERVE_NUM_ROBOT_HUMAN_DATA - len(values)
    if n:
        values += [robot_human_series_data[-1]] * n

    (robot_human_data_newest, robot_human_data_before1,
     robot_human_data_before2, robot_human_data_before3,
     robot_human_data_before4, robot_human_data_before5,
     robot_human_data_before6, robot_human_data_before7,
     robot_human_data_before8, robot_human_data_before9) = values

    tmp_human_comment = robot_human_data_newest.getHumanComment()

    config.debug_print("dialogue_algorithm_rulebase a")

    tmp_okao_data = robot_human_data_newest.getOkaoVisionData()

    config.debug_print("tmp_okao_data: " +str(tmp_okao_data))
    config.debug_print("dialogue_algorithm_rulebase b")
    config.debug_print("len(tmp_okao_data): " +str(len(tmp_okao_data)))

    tmp_okao_exist_data = [0,0,0,0,0,0,0]

    for var in range(len(tmp_okao_data)-1):
        config.debug_print("var:" +str(var))
        config.debug_print("tmp_okao_data[var][0]:" +tmp_okao_data[var][0])

        if not (0 == tmp_okao_data[var][0]):
            config.debug_print("dialogue_algorithm_rulebase tmp_okao_data var" +str(var))

            tmp_okao_exist_data = tmp_okao_data[var]
            break
        else:
            config.debug_print("decide_action_rulebase内、OKAOの読み取り値なし")

    config.debug_print("dialogue_algorithm_rulebase c")

    okao_age  = tmp_okao_exist_data[0]
    okao_gen  = tmp_okao_exist_data[1]
    okao_surp = tmp_okao_exist_data[2]
    okao_angr = tmp_okao_exist_data[3]
    okao_sadn = tmp_okao_exist_data[4]
    okao_happ = tmp_okao_exist_data[5]
    okao_neut = tmp_okao_exist_data[6]

    pic_term_list = pic_human_term(tmp_human_comment)

    config.debug_print("pic_term_list: " +str(pic_term_list))

    robot_comment_no = 0
    recog_commnet_skip_flag = 0

    print(robot_human_data_newest.getRobotComment())

    config.debug_print("robot_human_data_newest.getRobotComment(): " +str(robot_human_data_newest.getRobotComment()))
    config.debug_print("type(robot_human_data_newest.getRobotComment()): " + str(type(robot_human_data_newest.getRobotComment())))

    if (10001 == robot_human_data_newest.getRobotComment()):#10001:"こんにちは、お客様が来ていただけるのを、ずっとお待ちしておりました。本日はどちらからいらっしゃったんですか？",
        robot_comment_no = 10101#10101:"遠いところですか？",
        print("10001です。！！！！！！")

#コメント表、アクション表からどう取得するかを考える必要あり。
    elif (10001 == robot_human_data_before1.getRobotComment()):#10001:"こんにちは、お客様が来ていただけるのを、ずっとお待ちしておりました。本日はどちらからいらっしゃったんですか？",
        if(True == ("近い" in pic_term_list)):
            robot_comment_no = 10202#10202:"なーんだ、近いんですね。",
        else:
            robot_comment_no = 10201#10201:"遠いところからわざわざありがとうございます。",
        print("10001です。！！！！！！")

    elif (10001 == robot_human_data_before2.getRobotComment()):#10001:"こんにちは、お客様が来ていただけるのを、ずっとお待ちしておりました。本日はどちらからいらっしゃったんですか？",
        robot_comment_no = 10203#10202:"なーんだ、近いんですね。",
        print("10001です。！！！！！！")

    elif ((20001 == robot_human_data_newest.getRobotComment()) or (20002 == robot_human_data_newest.getRobotComment())):#20001:"私の鼻に何かついてませんか？よーく見てくれませんか？",
        print("20001です。！！！！！！")

        if(0 == okao_gen):#読み取り不能
            robot_comment_no = 20002#20002:"もう一回、私の鼻をよーく見て下さい",

        elif(1 == okao_gen):#男性
            if(okao_age <= 35):
                robot_comment_no = 20120#男性ハタチ
            elif(35 < okao_age <= 40):
                robot_comment_no = 20125#男性二十五歳
            elif(40 < okao_age <= 45):
                robot_comment_no = 20130#男性三十歳
            elif(45 < okao_age <= 50):
                robot_comment_no = 20135#男性三十五歳
            elif(50 < okao_age <= 55):
                robot_comment_no = 20140#男性四十歳
            elif(55 < okao_age):
                robot_comment_no = 20145#男性四十五歳
            else:
                print("男性、年齢文法エラー")

        elif(2 == okao_gen):#女性
            if(okao_age <= 35):
                robot_comment_no = 20220#女性ハタチ
            elif(35 < okao_age <= 40):
                robot_comment_no = 20225#女性二十五歳
            elif(40 < okao_age <= 45):
                robot_comment_no = 20230#女性三十歳
            elif(45 < okao_age <= 50):
                robot_comment_no = 20235#女性三十五歳
            elif(50 < okao_age <= 55):
                robot_comment_no = 20240#女性四十歳
            elif(55 < okao_age):
                robot_comment_no = 20245#女性四十五歳
            else:
                print("女性、年齢文法エラー")

        else:
            print("オカオ文法エラー")

    # ストーリー（あいさつ）1回目コメント選択（トリガーと顔判定）
    elif(True == ("こんにちは" in pic_term_list) or True == ("おはよう" in pic_term_list) or True == ("はじめまして" in pic_term_list) or True == ("お疲れ様" in pic_term_list) or True == ("かわいい" in pic_term_list) or True == ("おもしろ" in pic_term_list)):
        if(2 == okao_gen):  # 女性
            robot_comment_no = 101002
            recog_commnet_skip_flag = 1
        elif(0 == okao_gen or 1 == okao_gen):  # 男性or読み取り不能
            robot_comment_no = 101000
            recog_commnet_skip_flag = 1
        else:
            print("オカオ文法エラー")
    # ストーリー（あいさつ）2回目コメント選択（女性以外）
    elif (101000 == robot_human_data_newest.getRobotComment()):
        robot_comment_no = random.choice([102000,102010,102020,102030,102040,102050,102060,102070,102080,102090,102100,102110,102120,102130,102140])
        recog_commnet_skip_flag = 1
    # ストーリー（あいさつ）2回目コメント選択（女性）
    elif (101002 == robot_human_data_newest.getRobotComment()):
        robot_comment_no = random.choice([102002,102012,102022,102032,102042,102052,102062,102072,102082])
        recog_commnet_skip_flag = 1
    # ストーリー（あいさつ）3回目コメント選択（2つの質問のどちらかに分岐）
    elif (101000 == robot_human_data_before1.getRobotComment() or 101002 == robot_human_data_before1.getRobotComment()):
        robot_comment_no = random.choice([103000,106000])
    # ストーリー（あいさつ）4回目（6回目）コメント選択
    elif (103000 == robot_human_data_newest.getRobotComment()):
        robot_comment_no = 104000
    # ストーリー（あいさつ）5回目（7回目）コメント選択
    elif (104000 == robot_human_data_newest.getRobotComment()):
        if(True == ("遠い" in pic_term_list)):
            robot_comment_no = 105000
            recog_commnet_skip_flag = 1
        elif(True == ("近い" in pic_term_list)):
            robot_comment_no = 105010
            recog_commnet_skip_flag = 1
        else:
            robot_comment_no = 105020
            recog_commnet_skip_flag = 1
    # ストーリー（あいさつ）6回目（8回目）コメント選択
    elif (105000 <= robot_human_data_newest.getRobotComment() <= 105020):
        if (106000 == robot_human_data_before4.getRobotComment()):  # 2つ目の質問が既に終わっている場合締めへ
            robot_comment_no = 108000
        else:                                                       # 終わっていなければ、2つ目の質問へ
            robot_comment_no = 106000
    # ストーリー（あいさつ）7回目（4回目）コメント選択
    elif (106000 == robot_human_data_newest.getRobotComment()):
        if(True == ("秘密" in pic_term_list)):
            robot_comment_no = 107000
            recog_commnet_skip_flag = 1
        else:
            robot_comment_no = random.choice([107010,107020,107030])
            recog_commnet_skip_flag = 1
    # ストーリー（あいさつ）8回目（5回目）コメント選択
    elif (107000 <= robot_human_data_newest.getRobotComment() <= 107030):
        if (103000 == robot_human_data_before4.getRobotComment()):  # 1つ目の質問が既に終わっている場合締めへ
            robot_comment_no = 108000
        else:                                                       # 終わっていなければ、1回目の質問へ
            robot_comment_no = 103000



    elif(True == ("さようなら" in pic_term_list)):
        robot_comment_no = random.choice([21])
    elif(True == ("私は" in pic_term_list)) and (True == ("と言います" in pic_term_list)):
        robot_comment_no = random.choice([41])
    elif(True == ("元気" in pic_term_list)):
        robot_comment_no = random.choice([101,102,103,104])
    elif(True == ("本当に" in pic_term_list)):
        robot_comment_no = random.choice([105,106,107])
    elif(True == ("冗談" in pic_term_list)):
        robot_comment_no = random.choice([105,106,107])
    elif(True == ("すごい" in pic_term_list)):
        robot_comment_no = random.choice([108,109,110,203,204])
    elif(True == ("さむい" in pic_term_list)):
        robot_comment_no = random.choice([111,112,113])
    elif(True == ("ありがとう" in pic_term_list)):
        robot_comment_no = random.choice([114,115,116])
    elif(True == ("自己紹介" in pic_term_list)):
        robot_comment_no = random.choice([117,118])
    elif(True == ("あなた" in pic_term_list)) and (True == ("だれ" in pic_term_list)):
        robot_comment_no = random.choice([117,118])
    elif(True == ("あなた" in pic_term_list)) and (True == ("人間" in pic_term_list)):
        robot_comment_no = random.choice([117,118,119,120])
    elif(True == ("もっと" in pic_term_list)) and (True == ("褒めて" in pic_term_list)):
        robot_comment_no = random.choice([121,122])
    elif(True == ("あなた" in pic_term_list)) and (True == ("素敵" in pic_term_list)):
        robot_comment_no = random.choice([123,124])
    elif(True == ("あなた" in pic_term_list)) and (True == ("元気" in pic_term_list)):
        robot_comment_no = random.choice([125,126])
    elif(True == ("上手" in pic_term_list)):
        robot_comment_no = random.choice([127,128,129,130])
    elif(True == ("空腹" in pic_term_list)):
        robot_comment_no = random.choice([201,202])
    elif(True == ("人が多い" in pic_term_list)):
        robot_comment_no = random.choice([205,206])

    elif(True == ("年齢" in pic_term_list)) and (True == ("当て" in pic_term_list)):
        robot_comment_no = 20001
    elif(True == ("いくつに見える" in pic_term_list)):
        robot_comment_no = 20001

    else:
        pass

    config.debug_print("dialogue_algorithm_rulebase関数の中の最後でのrobot_comment_no: " +str(robot_comment_no))

    return (robot_comment_no, recog_commnet_skip_flag)


def decide_action_rulebase(robot_human_series_data):

    config.debug_print("decide_action_rulebaseが呼べてます。")

    robot_action = [0,0,0,0]#ロボットのコメント、モーション、LEDの、それぞれのテーブルのID

    robot_comment_no, recog_commnet_skip_flag = dialogue_algorithm_rulebase(robot_human_series_data)
    config.debug_print("decide_actionの中で、dialogue_algorithm_rulebase関数終了")

    robot_motion_no = random.randrange(1,config.NUM_OF_CHOICES_MOTION+1)
    robot_motion_no = random.randrange(1,4)

    robot_led_no = random.randrange(1,config.NUM_OF_CHOICES_LED+1)
    robot_led_no = random.randrange(1,4)

    robot_action = [robot_comment_no,robot_motion_no,robot_led_no,recog_commnet_skip_flag]

    config.debug_print("decide_action_rulebase b")

    return robot_action

if __name__ == '__main__':
    tmp_term = "寒いね"
    tmp_robo_term = "ロボットロボロボ"

    print("tmp_term: ", tmp_term)

    print("pic_human_term(tmp_term)", pic_human_term(tmp_term))

    tmp_robo_h_s_data = []
    tmp = robo_human_data.RobotHumanData()
    tmp.setHumanComment(tmp_term)
    tmp_robo_h_s_data.append(tmp)

    tmp.setRobotComment(tmp_robo_term)

    reta,retb = dialogue_algorithm_rulebase(tmp_robo_h_s_data)
    print("dialogue_algorithm_rulebaseの返り値", reta,retb)

    ret = decide_action_rulebase(tmp_robo_h_s_data)
    print ("decide_action_rulebase関数の返り値" ,ret)
