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
#TAT_ACTION_LOG = 'tat_action_log.csv'

def argmax_ndim(arg_array):
    return np.unravel_index(arg_array.argmax(), arg_array.shape)

def calc_reward(face_data):
    weight_array=np.array([0,100,40,-50,-50])
    #[neutral,happy,surprise,angry,sad]
    reward=np.dot(face_data,weight_array)
    return reward

def predict(face, situation, action, id_number):
    #TODO:dummy just now
    face_array_size=5
    #read trained weights based on id_number
    predicted = np.random.uniform(low=0,high=1,size=face_array_size)
    return predicted

def face_predict(input_data, action_candidate):
    face = input_data.okao_list
    situation=[input_data.time_stamp,
        input_data.day_of_week,
        input_data.weather_data]
    action = [action_candidate.robot_comment, action_candidate.robot_motion, action_candidate.robot_led]
    id_number = 0 #not be defined
    #predicted_face = predict(face, action, id_number)
    predicted_face = predict(face, situation, action, id_number)

    return predicted_face

#convert from tat number to jbc number
def tat2jbc_comment_num(tat_comment_num):
    tat2jbc=tbl_tat_comment.tblRoboComeTAT()
    jbc_num=tat2jbc.DATA[tat_comment_num,1]
    return str(jbc_num)

def jbc2tat_comment_num(jbc_comment_num):
    tat2jbc=tbl_tat_comment.tblRoboComeTAT()
    print('jbc_comment_num',jbc_comment_num)
    print('comment',tat2jbc.DATA[0,0])
    for array_num in range(tat2jbc.DATA.shape[0]):
        if jbc_comment_num == tat2jbc.DATA[array_num,1]:
            tat_num = array_num

    return tat_num




def update_TATreward_table(str_reward_table, selected_action, tmp_human_face):
    # read reward table from csv file
    #tat_reward_table = np.load(str_reward_table,delimiter=",")
    tat_reward_table = np.load(str_reward_table)

    # devide array of action into num of comment/motion/led
    comment, motion, led = selected_action

    # calculate evaluation by human
    level = calc_reward(tmp_human_face)

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
        tmp_human_face = robot_human_data_newest.getOkaoVisionData()

        print('getRobotCommennt()',robot_human_data_before1.getRobotComment())
        selected_action = np.array([jbc2tat_comment_num(robot_human_data_before1.getRobotComment()),
            robot_human_data_before1.getRobotMotion(),
            robot_human_data_before1.getRobotLed()])

        # update reward table
        update_TATreward_table(TAT_REWARD_TBL, selected_action, tmp_human_face)

    # read updated reward table to select action
    #tat_reward_table = np.load(TAT_REWARD_TBL,delimiter=",")
    tat_reward_table = np.load(TAT_REWARD_TBL)


    # check the key of human's comment
    pic_term_list = pic_human_term(tmp_human_comment)

    # start when the comment of human is konnichiwa
    if(True == ("こんにちは" in pic_term_list)):
        #select argmax
        robot_action = argmax_ndim(tat_reward_table)
        robot_comment_no = tat2jbc_comment_num(robot_action[0])

    #robot_action = [robot_comment_no,robot_motion_no,robot_led_no]

    return robot_action

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
    robot_human_series_data[1].robot_comment = 30101
    robot_human_series_data[1].robot_motion = 0
    robot_human_series_data[1].robot_led = 1

    robot_human_series_data[0].human_comment = "こんにちは"
    robot_human_series_data[0].okao_data = [[100,0,0,0,0]]

    print("action_is",decide_action_TATsys(robot_human_series_data))
