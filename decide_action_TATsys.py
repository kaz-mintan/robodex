# coding:utf-8
#decide_action_TATsys.py
#関数よりクラスの方が良いのかな？
import tbl_human_comment
import tbl_robo_comment
import config

import numpy as np
from numpy.random import *
import itertools

import tbl_robo_led
import tbl_robo_motion
import tbl_tat_comment

import robo_human_data

from decide_action_rulebase import pic_human_term
import config

import recog_okao
import random

## to debug by kuma
import csv
from datetime import datetime

#iinoka
TAT_REWARD_TBL = 'tat_reward_tbl.npy'
HAPPY_THRESHOLD = 40 #60
HAPPY_RATE = 35 #%
#TAT_ACTION_LOG = 'tat_action_log.csv'

def argmax_ndim(arg_array):
    return np.unravel_index(arg_array.argmax(), arg_array.shape)

def calc_reward(face_data):
    weight_array=np.array([0,100,40,-50,-50])
    #[neutral,happy,surprise,angry,sad]
    print('face_data',face_data)
    reward=np.dot(face_data,weight_array)
    return reward

def predict(face, situation, action, id_number):
    #TODO:dummy just now
    face_array_size=5
    #read trained weights based on id_number
    predicted = np.random.uniform(low=0,high=1,size=face_array_size)
    return predicted

def face_predict(input_data, action_candidate):
    face = input_data.getOkaoVisionData()#komatsu
    situation=[input_data.getTimeStamp(),#komatsu
        input_data.getDayOfWeek(),#komatsu
        input_data.getWheatherSimpleToday()]#komatsu
#    face = input_data.okao_list
#    situation=[input_data.time_stamp,
#        input_data.day_of_week,
#        input_data.weather_data]

    action = [action_candidate.robot_comment, action_candidate.robot_motion, action_candidate.robot_led]
    id_number = 0 #not be defined
    predicted_face = predict(face, situation, action, id_number)

    return predicted_face

#convert from tat number to jbc number
def tat2jbc_comment_num(tat_comment_num):
    tat2jbc=tbl_tat_comment.tblRoboComeTAT()
    jbc_num=tat2jbc.DATA[tat_comment_num,1]
    return str(jbc_num)

def jbc2tat_comment_num(jbc_comment_num):
    tat2jbc=tbl_tat_comment.tblRoboComeTAT()
    for array_num in range(tat2jbc.DATA.shape[0]):
        if jbc_comment_num == tat2jbc.DATA[array_num,1]:
            tat_num = array_num

    return tat_num

def update_TATreward_table(str_reward_table, selected_action, tmp_human_face):
    # read reward table from csv file
    tat_reward_table = np.load(str_reward_table)

    # devide array of action into num of comment/motion/led
    comment, motion, led = selected_action

    # calculate evaluation by human
    level = calc_reward(tmp_human_face)
    print('level',level)

    # update reward table
    tat_reward_table=tat_reward_table-level*np.ones_like(tat_reward_table)
    tat_reward_table[comment,motion,led] += level

    # save the updated reward table
    np.save(str_reward_table,tat_reward_table)

# simple evaluator based on facial expression
def eval_face(face):
    happy_point = 0
    for time in range(len(face)-1):
        if not (0 == face[time][0]):
            tmp_face_data = face[time]
            if tmp_face_data[5]>HAPPY_THRESHOLD:
                happy_point+=1
        else:
            tmp_face_data = [0,0,0,0,0,0,0]

    print('tat_debug/eval_face/face',face)
    if happy_point > len(face)*0.01*HAPPY_RATE:
        evaluation = 'good'
    else:
        evaluation = 'bad'
    print('tat_debug/eval_face/evaluation',evaluation)
    return evaluation

## returns the number of same comment which was selected before
def return_past_num(robot_human_data_newest,robot_human_data_before,before_num):
    #any past data
    #if robot_human_data_newest.getRobotComment() == robot_human_data_before.getRobotComment():
    #pic_term_list = pic_human_term(tmp_human_comment)
    if pic_human_term(robot_human_data_newest.getHumanComment()) == pic_human_term(robot_human_data_before.getHumanComment()):
        past_num = before_num
    else:
        # if there is NO COMMENT which was selected before
        past_num = 0

    #past_num is the number which contains the same robot comment of the robot_human_data_newest
    print('tat_debug/return_post_num/past_num',past_num)
    return past_num

## returns the number of comment which was selected before OR random
def ret_comment_num(values):
    global comment_num
    global rule
    global face
    #global writer_face

    robot_human_data_newest = values[0]
    n = len(values)

    #for i in reversed(range(1,n)):
    for i in range(1,n):
        #past_num=return_past_num(robot_human_data_newest,values[i],i)
        past_num=return_past_num(values[0],values[i],i)
        #print('tat_debug/ret_comment_num/values',values[i].getRobotComment())

        with open('past_selected_number.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(['past_num','comment_number',datetime.now()])
            writer.writerow([past_num-1, values[past_num-1].getRobotComment()])

        if past_num!=0:
            rule = 'past'
            past_number = past_num-1
            break
            #the number could be the latest number
        else:
            rule = 'random'
            past_number = None

    if rule != 'random':
        face = values[past_number].getOkaoVisionData()

        with open('refered_face.csv','a') as f_face:
            writer_face = csv.writer(f_face)
            writer_face.writerow(['okao_age','okao_gen','okao_surp','okao_anger','okao_sadn','okao_happ','okao_neut]',datetime.now()])
            #writer_facce.writerow([face[0],face[1],face[2],face[3],face[4],face[5],face[6]])
            writer_face.writerow(face)

        #face = values[past_number].setOkaoVisionData(recog_okao.okao_data)
        if eval_face(face)=='good':
            rule = 'past'
            comment_num = values[past_number].getRobotComment()

        else:
            rule = 'random'
            comment_num = None
    #comment_num = None
    print('tat_debug/ret_comment_num/comment_num',comment_num)
    return rule, comment_num

# instead of random.choice(comment_list)
# CAUTION! there ARE two additional arguments
def tat_choice(comment_list,past_rule,past_comment):
    if past_rule == 'random':
        chosen_number = random.choice(comment_list)
    else:
        chosen_number = past_comment

    return chosen_number

#this is dialogue for tat sys demonstration
def dialogue_algorithm_TATsys(robot_human_series_data):
#tbl_robo_commentの中を参照して、robot_commentを返す。
    print("dialogue_algorithm_TATsysが呼べてます。")

    # separate given data into time series parts
    values = robot_human_series_data[:config.RESERVE_NUM_ROBOT_HUMAN_DATA]#下の書き方でも良いが、robot_human_series_dataの大きさがRESERVE_NUM_ROBOT_HUMAN_DATAより大きくなってしまった時（バグ）の保険のため

    n = config.RESERVE_NUM_ROBOT_HUMAN_DATA - len(values)
    if n:
        values += [robot_human_series_data[-1]] * n

    past_rule , past_comment = ret_comment_num(values)
    print('tat_debug/dialogue.../past_rule,',past_rule,'past_comment',past_comment)

    (robot_human_data_newest, robot_human_data_before1,
     robot_human_data_before2, robot_human_data_before3,
     robot_human_data_before4, robot_human_data_before5,
     robot_human_data_before6, robot_human_data_before7,
     robot_human_data_before8, robot_human_data_before9) = values

    tmp_human_comment = robot_human_data_newest.getHumanComment()

    print("dialogue_algorithm_rulebase a")

    #tmp_okao_data = robot_human_data_newest.setOkaoVisionData(recog_okao.okao_data)

    #print("tmp_okao_data:",tmp_okao_data)
    print("dialogue_algorithm_rulebase b")
    print("len(tmp_okao_data):",len(tmp_okao_data))

    for var in range(len(tmp_okao_data)-1):
        print("var:",var)
        print("tmp_okao_data[var][0]:",tmp_okao_data[var][0])

        if not (0 == tmp_okao_data[var][0]):
            print("dialogue_algorithm_rulebase tmp_okao_data",var)

            tmp_okao_exist_data = tmp_okao_data[var]
            break
        else:
            tmp_okao_exist_data = [0,0,0,0,0,0,0]
            print("decide_action_rulebase内、OKAOの読み取り値なし")

    print("dialogue_algorithm_rulebase c")

    okao_age  = tmp_okao_exist_data[0]
    okao_gen  = tmp_okao_exist_data[1]
    okao_surp = tmp_okao_exist_data[2]
    okao_angr = tmp_okao_exist_data[3]
    okao_sadn = tmp_okao_exist_data[4]
    okao_happ = tmp_okao_exist_data[5]
    okao_neut = tmp_okao_exist_data[6]

    pic_term_list = pic_human_term(tmp_human_comment)

    if (1 == config.DEBUG_PRINT):
        print(pic_term_list)

    robot_comment_no = 0
    recog_commnet_skip_flag = 0

    print(robot_human_data_newest.getRobotComment())

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
        #robot_comment_no = random.choice([102000,102010,102020,102030,102040,102050,102060,102070,102080,102090,102100,102110,102120,102130,102140])
        robot_comment_no = tat_choice([102000,102010,102020,102030,102040,102050,102060,102070,102080,102090,102100,102110,102120,102130,102140],past_rule,past_comment)

    #def tat_choice(comment_list,past_rule,past_comment):
        recog_commnet_skip_flag = 1
    # ストーリー（あいさつ）2回目コメント選択（女性）
    elif (101002 == robot_human_data_newest.getRobotComment()):
        robot_comment_no = tat_choice([102002,102012,102022,102032,102042,102052,102062,102072,102082],past_rule,past_comment)
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
            #robot_comment_no = random.choice([107010,107020,107030])
            robot_comment_no = tat_choice([107010,107020,107030],past_rule,past_comment)
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
        #robot_comment_no = random.choice([101,102,103,104])
        robot_comment_no = tat_choice([101,102,103,104],past_rule,past_comment)
    elif(True == ("本当に" in pic_term_list)):
        robot_comment_no = tat_choice([105,106,107],past_rule,past_comment)
    elif(True == ("冗談" in pic_term_list)):
        robot_comment_no = tat_choice([105,106,107],past_rule,past_comment)
    elif(True == ("すごい" in pic_term_list)):
        robot_comment_no = tat_choice([108,109,110,203,204],past_rule,past_comment)
    elif(True == ("さむい" in pic_term_list)):
        robot_comment_no = tat_choice([111,112,113],past_rule,past_comment)
    elif(True == ("ありがとう" in pic_term_list)):
        robot_comment_no = tat_choice([114,115,116],past_rule,past_comment)
    elif(True == ("自己紹介" in pic_term_list)):
        robot_comment_no = tat_choice([117,118],past_rule,past_comment)
    elif(True == ("あなた" in pic_term_list)) and (True == ("だれ" in pic_term_list)):
        robot_comment_no = tat_choice([117,118],past_rule,past_comment)
    elif(True == ("あなた" in pic_term_list)) and (True == ("人間" in pic_term_list)):
        robot_comment_no = tat_choice([117,118,119,120],past_rule,past_comment)
    elif(True == ("もっと" in pic_term_list)) and (True == ("褒めて" in pic_term_list)):
        robot_comment_no = tat_choice([121,122],past_rule,past_comment)
    elif(True == ("あなた" in pic_term_list)) and (True == ("素敵" in pic_term_list)):
        robot_comment_no = tat_choice([123,124],past_rule,past_comment)
    elif(True == ("あなた" in pic_term_list)) and (True == ("元気" in pic_term_list)):
        robot_comment_no = tat_choice([125,126],past_rule,past_comment)
    elif(True == ("上手" in pic_term_list)):
        robot_comment_no = tat_choice([127,128,129,130],past_rule,past_comment)
    elif(True == ("空腹" in pic_term_list)):
        robot_comment_no = tat_choice([201,202],past_rule,past_comment)
    elif(True == ("人が多い" in pic_term_list)):
        robot_comment_no = tat_choice([205,206],past_rule,past_comment)

    elif(True == ("年齢" in pic_term_list)) and (True == ("当て" in pic_term_list)):
        robot_comment_no = 20001
    elif(True == ("いくつに見える" in pic_term_list)):
        robot_comment_no = 20001

    else:
        pass

    print("ダイアログの中のrobot_commnet_no")
    print(robot_comment_no)

    return (robot_comment_no, recog_commnet_skip_flag)

def tmp_dev_function(robot_human_series_data):
    values = robot_human_series_data[:config.RESERVE_NUM_ROBOT_HUMAN_DATA]
    n = config.RESERVE_NUM_ROBOT_HUMAN_DATA - len(values)
    if n:
        values += [robot_human_series_data[-1]] * n
    a,b =ret_comment_num(values)
    return a,b


def decide_action_TATsys(robot_human_series_data):

    robot_action = [0,0,0,0]#ロボットのコメント、モーション、LEDの、それぞれのテーブルのID

    robot_comment_no, recog_commnet_skip_flag = dialogue_algorithm_TATsys(robot_human_series_data)
    #at this point
    robot_motion_no=0
    robot_led_no=0

    robot_action = [robot_comment_no,robot_motion_no,robot_led_no,recog_commnet_skip_flag]

    with open('selected_action.csv','a') as f_action:
            writer_act = csv.writer(f_action)
            writer_act.writerow(['comment','motion','led','skip_flg',datetime.now()])
            writer_act.writerow(robot_action)

    return robot_action

if __name__ == "__main__" :

    robot_human_series_data = [robo_human_data.RobotHumanData(),
            robo_human_data.RobotHumanData(),
            robo_human_data.RobotHumanData(),
            robo_human_data.RobotHumanData(),
            robo_human_data.RobotHumanData(),
            robo_human_data.RobotHumanData(),
            robo_human_data.RobotHumanData(),
            robo_human_data.RobotHumanData(),
            robo_human_data.RobotHumanData(),
            robo_human_data.RobotHumanData()]

    robot_human_series_data[0].human_comment = "すごい"
    robot_human_series_data[0].okao_data = [[20,2,0,0,0,94,0],[20,2,0,0,0,90,0],[20,2,0,0,0,70,0],[20,2,0,0,0,100,0]]
    robot_human_series_data[0].robot_comment = 109
    #robot_human_series_data[0].robot_comment = 103000 #"今日はどちらからお越しですか？",

    robot_human_series_data[1].human_comment = "すごい"
    robot_human_series_data[1].robot_comment = 203
    robot_human_series_data[1].recogt_commnet_skip_flag = 0
    robot_human_series_data[1].okao_data = [[20,2,0,0,0,20,0],[20,2,0,0,0,90,0],[20,2,0,0,0,70,0],[20,2,0,0,0,100,0]]

    robot_human_series_data[2].human_comment = "すごい"
    #robot_human_series_data[2].human_comment = "こんにちは"
    robot_human_series_data[2].robot_comment = 0
    robot_human_series_data[2].recogt_commnet_skip_flag = 1
    robot_human_series_data[2].okao_data = [[20,2,0,0,0,30,0],[20,2,0,0,0,90,0],[20,2,0,0,0,70,0],[20,2,0,0,0,100,0]]

    robot_human_series_data[3].human_comment = ""
    robot_human_series_data[3].robot_comment = 107030 #107030:"とても素敵なお名前ですね。あなたの発明で世界は革新するのですね。スティーブジョブスを超えるかたですね。", # その他
    robot_human_series_data[3].robot_comment = 108000
    robot_human_series_data[3].okao_data = [[20,2,0,0,0,40,0],[20,2,0,0,0,90,0],[20,2,0,0,0,70,0],[20,2,0,0,0,100,0]]

    robot_human_series_data[4].human_comment = "くまがいです"
    robot_human_series_data[4].robot_comment = 106000 #106000:"お名前をお聞かせください。",
    robot_human_series_data[4].recogt_commnet_skip_flag = 1
    robot_human_series_data[4].okao_data = [[20,2,0,0,0,50,0],[20,2,0,0,0,90,0],[20,2,0,0,0,70,0],[20,2,0,0,0,100,0]]

    robot_human_series_data[5].human_comment = ""
    robot_human_series_data[5].robot_comment = 105000 #105000:"わざわざ遠くからせんぱいに来てもらえるなんて、ぼくはなんて幸せものなんでしょう。アールツーディーツーにも負けません。", # 遠い
    robot_human_series_data[5].okao_data = [[20,2,0,0,0,60,0],[20,2,0,0,0,90,0],[20,2,0,0,0,70,0],[20,2,0,0,0,100,0]]

    robot_human_series_data[6].human_comment = "遠い"
    robot_human_series_data[6].robot_comment = 10101 #10101:"遠いところですか？",
    robot_human_series_data[6].recogt_commnet_skip_flag = 1
    robot_human_series_data[6].okao_data = [[20,2,0,0,0,70,0],[20,2,0,0,0,90,0],[20,2,0,0,0,70,0],[20,2,0,0,0,100,0]]

    robot_human_series_data[7].human_comment = "カナダ"
    robot_human_series_data[7].robot_comment = 103000 #"今日はどちらからお越しですか？",
    robot_human_series_data[7].recogt_commnet_skip_flag = 0
    robot_human_series_data[7].okao_data = [[20,2,0,0,0,80,0],[20,2,0,0,0,90,0],[20,2,0,0,0,70,0],[20,2,0,0,0,100,0]]

    robot_human_series_data[8].human_comment = ""
    robot_human_series_data[8].robot_comment = 101002
    #101002:"僕は太鼓持ちロボットティーティーエムゼロスリーです。あなたのために生まれてきたロボットです。",
    robot_human_series_data[8].okao_data = [[20,2,0,0,0,80,0],[20,2,0,0,0,90,0],[20,2,0,0,0,70,0],[20,2,0,0,0,100,0]]

    robot_human_series_data[9].human_comment = "こんにちは"
    #robot_human_series_data[9].robot_comment = 101002
    robot_human_series_data[9].recogt_commnet_skip_flag = 1
    robot_human_series_data[9].okao_data = [[20,2,0,0,0,80,0],[20,2,0,0,0,90,0],[20,2,0,0,0,70,0],[20,2,0,0,0,100,0]]

    decide_action_TATsys(robot_human_series_data)
