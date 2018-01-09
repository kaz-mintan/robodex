# coding:utf-8
#decide_action_TATsys.py
#関数よりクラスの方が良いのかな？
import numpy as np
from numpy.random import *
import itertools

import tbl_robo_comment
import tbl_robo_led
import tbl_robo_motion
import tbl_tat_comment

import robo_human_data

from decide_action_rulebase import pic_human_term
import config

#iinoka
TAT_REWARD_TBL = 'tat_reward_tbl.npy'
HAPPY_THRESHOLD = 60
HAPPY_RATE = 50 #%
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

def decide_action_TATsys(robot_human_series_data):

    # extract human's comment (copied from rulebase.py)
    data_len=len(robot_human_series_data)

    if data_len == 1:
        robot_human_data_newest = robot_human_series_data[-1]

        tmp_human_comment = robot_human_data_newest.getHumanComment()
        tmp_human_face = robot_human_data_newest.getOkaoVisionData()

        #skip updating reward table

    if data_len >=2:

        values = robot_human_series_data[:2]
        (robot_human_data_newest, robot_human_data_before1) = values

        tmp_human_comment = robot_human_data_newest.getHumanComment()
        eval_human_face = robot_human_data_before1.getOkaoVisionData()

        selected_action = np.array([jbc2tat_comment_num(robot_human_data_before1.getRobotComment()),
            robot_human_data_before1.getRobotMotion(),
            robot_human_data_before1.getRobotLed()])

        # update reward table
        update_TATreward_table(TAT_REWARD_TBL, selected_action, eval_human_face)

    # read updated reward table to select action
    tat_reward_table = np.load(TAT_REWARD_TBL)


    # check the key of human's comment
    pic_term_list = pic_human_term(tmp_human_comment)

    # start when the comment of human is konnichiwa
    if(True == ("こんにちは" in pic_term_list)):
        #select argmax
        robot_action = argmax_ndim(tat_reward_table)
        robot_comment_no = tat2jbc_comment_num(robot_action[0])

    return robot_action

# simple evaluator based on facial expression
def eval_face(face):
    for time in range(len(face)-1):
        if not (0 == face[time][0]):
            tmp_face_data = face[time]
            if tmp_face_data[5]>HAPPY_THRESHOLD:
                happy_point+=1
        else:
            tmp_face_data = [0,0,0,0,0,0,0]
            print("decide_action_rulebase内、OKAOの読み取り値なし")

    if happy_point > len(face)*0.01*HAPPY_RATE:
        evaluation = 'good'
    else:
        evaluation = 'bad'
    return evaluation

## returns the number of same comment which was selected before
def return_past_num(robot_human_data_newest,robot_human_data_before,check_num):
    #any past data
    if robot_human_data_newest.getRobotComment() == robot_human_data_before.getRobotComment():
        past_num = check_num
    else:
        # if there is NO COMMENT which was selected before
        past_num = 0

    #past_num is the number which contains the same robot comment of the robot_human_data_newest
    return past_num

## returns the number of comment which was selected before OR random
def ret_comment_num(values):
    (robot_human_data_newest, robot_human_data_before[1],
     robot_human_data_before[2], robot_human_data_before[3],
     robot_human_data_before[4], robot_human_data_before[5],
     robot_human_data_before[6], robot_human_data_before[7],
     robot_human_data_before[8], robot_human_data_before[9]) = values

    for i in xrange(n):
        past_num[i]=return_past_num(robot_human_data_newest,robot_human_data_before[i],i)

        if past_num[i]!=0:
            past_number = past_num[i]
            #the number could be the latest number
        else:
            rule = 'random'
            comment_num = None

    if rule != 'random':
        face = robot_human_data_before[past_num].getOkaoVisionData()
        if eval_face(face)=='good':
            rule = 'past'
            comment_num = robot_human_data_before[past_num].getRobotComment()

        else:
            rule = 'random'
            comment_num = None
    return rule, comment_num

# instead of random.choice(comment_list)
# CAUTION! there ARE two additional arguments
def tat_choice(comment_list,past_rule,past_comment):
    chosen_number = 30201
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

    past_rule , past_comment = ret_past_num(values)



    (robot_human_data_newest, robot_human_data_before1,
     robot_human_data_before2, robot_human_data_before3,
     robot_human_data_before4, robot_human_data_before5,
     robot_human_data_before6, robot_human_data_before7,
     robot_human_data_before8, robot_human_data_before9) = values

    tmp_human_comment = robot_human_data_newest.getHumanComment()

    print("dialogue_algorithm_rulebase a")

    tmp_okao_data = robot_human_data_newest.getOkaoVisionData()

    print("tmp_okao_data:",tmp_okao_data)
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

    print(robot_human_data_newest.getRobotComment())

    if (10001 == robot_human_data_newest.getRobotComment()):#10001:"こんにちは、お客様が来ていただけるのを、ずっとお待ちしておりました。本日はどちらからいらっしゃったんですか？",
        robot_comment_no = 10101#10101:"遠いところですか？",
        print("10001です。！！！！！！")

    elif(True == ("なかいい" in pic_term_list)):
        robot_comment_no = random.choice([60000])


    elif(True == ("会長" in pic_term_list) or True == ("お願い" in pic_term_list)):
        robot_comment_no = random.choice([50000])

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

    elif(True == ("こんにちは" in pic_term_list) or True == ("おはよう" in pic_term_list) or True == ("はじめまして" in pic_term_list) or True == ("お疲れ様" in pic_term_list)):
        robot_comment_no = random.choice([21])

        if(0 == okao_gen):#読み取り不能
            robot_comment_no = random.choice([30101,30102,30103,30104,30105,30106,30107,30108,30109,30110,30111,30112,30113,30114,30115,30116,30117,30118])

        elif(1 == okao_gen):#男性
            robot_comment_no = random.choice([30101,30102,30103,30104,30105,30106,30107,30108,30109,30110,30111,30112,30113,30114,30115,30116,30117,30118])

        elif(2 == okao_gen):#女性
            robot_comment_no = random.choice([31101,31102,31103,31104,31105,31106,31107,31108,31109])
        else:
            print("オカオ文法エラー")

    elif ((30101 <= robot_human_data_newest.getRobotComment() <= 30118) or (31101 <= robot_human_data_newest.getRobotComment() <= 31119)):
        #robot_comment_no = random.choice([30201,30501])
        #TODO


        robot_comment_no = tat_choice([30201,30501])


    elif (30201 == robot_human_data_newest.getRobotComment()):
        robot_comment_no = random.choice([30301])

    elif (30301 == robot_human_data_newest.getRobotComment()):
        if(True == ("遠い" in pic_term_list)):
            robot_comment_no = 30401
        elif(True == ("近い" in pic_term_list)):
            robot_comment_no = 30402
        else:
            robot_comment_no = 30403

    elif (30401 <= robot_human_data_newest.getRobotComment() <=30403):
        if (30501 == robot_human_data_before4.getRobotComment()):
            robot_comment_no = 30701
        else:
            robot_comment_no = 30501

    elif (30501 == robot_human_data_newest.getRobotComment()):
        if(True == ("秘密" in pic_term_list)):
            robot_comment_no = 30601
        else:
            robot_comment_no = 30602

    elif (30601 <= robot_human_data_newest.getRobotComment() <=30602):
        if (30201 == robot_human_data_before4.getRobotComment()):
            robot_comment_no = 30701
        else:
            robot_comment_no = 30201

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

    print("ダイアログの中のrobot_commnet_no")
    print(robot_comment_no)

    return robot_comment_no




if __name__ == "__main__" :
    # initialization
    comment = tbl_tat_comment.tblRoboComeTAT()
    motion = tbl_robo_motion.tblRobotSRV()
    led = tbl_robo_led.tblRobotLED()

    #class tblRoboComeTAT:
    possible_range_comment=len(comment.DATA)
    possible_range_motion=len(motion.DATA)
    possible_range_led=len(led.DATA)

    reward = np.zeros((possible_range_comment,possible_range_motion,possible_range_led))

    np.save(TAT_REWARD_TBL,reward)
    robot_human_series_data = [robo_human_data.RobotHumanData()]

    robot_human_series_data[0].human_comment = "こんにちは"
    robot_human_series_data[0].okao_data = [[100,0,0,0,0]]

    print("action_is",decide_action_TATsys(robot_human_series_data))

    robot_human_series_data = [robo_human_data.RobotHumanData(),
            robo_human_data.RobotHumanData()]
    robot_human_series_data[1].human_comment = "こんにちは"
    robot_human_series_data[1].okao_data = [[0,100,0,0,0]]
    robot_human_series_data[1].robot_comment = 30103
    robot_human_series_data[1].robot_motion = 0
    robot_human_series_data[1].robot_led = 1

    robot_human_series_data[0].human_comment = "こんにちは"
    robot_human_series_data[0].okao_data = [[100,0,0,0,0]]

    print("action_is",decide_action_TATsys(robot_human_series_data))
