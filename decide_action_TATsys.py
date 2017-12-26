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
#iinoka

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
    tat2jbc=tblRoboComeTAT()
    jbc_num=tat2jbc.DATA[tat_comment_num,1]
    return jbc_num


def decide_action_TATsys(robot_human_series_data):
    # initialize
    action_candidate = robo_human_data.RobotHumanData()

    comment = tblRoboComeTAT()
    motion = tblRobotSRV()
    led = tblRobotLED()

    possible_range_comment=len(comment.DATA)
    possible_range_motion=len(motion.DATA)
    possible_range_led=len(led.DATA)

    reward=np.zeros((possible_range_comment,possible_range_motion,possible_range_led))

    # extract human's comment copied from rulebase.py
    values = robot_human_series_data[:config.RESERVE_NUM_ROBOT_HUMAN_DATA]
    n = config.RESERVE_NUM_ROBOT_HUMAN_DATA - len(values)
    if n:
        values += [robot_human_series_data[-1]] * n
    (robot_human_data_newest,\
            robot_human_data_before1,\
            robot_human_data_before2,\
            robot_human_data_before3,\
            robot_human_data_before4,\
            robot_human_data_before5,\
            robot_human_data_before6,\
            robot_human_data_before7,\
            robot_human_data_before8,\
            robot_human_data_before9) = values

    tmp_human_comment = robot_human_data_newest.getHumanComment()

    pic_term_list = pic_human_term(tmp_human_comment)

    # start when the comment of human is konnichiwa
    if(True == ("こんにちは" in pic_term_list) in pic_term_list):

        #select argmax
        robot_action = argmax_ndim(reward)
        #print(robot_action)

    robot_action = [robot_comment_no,robot_motion_no,robot_led_no]

    return robot_action

def update_reward_table(str_reward_table, selected_action, robot_human_data,level=50):
    #read reward table from csv file
    tat_reward_table = np.loadtxt(str_reward_table,delimiter=",")

    #devide arguments
    comment, motion, led = selected_action

    #update reward table
    tat_reward_table=tat_reward_table-level*np.ones_like(tat_reward_table)
    tat_reward_table[comment,motion,led] += level

    return table

if __name__ == "__main__" :
    robot_human_series_data = robo_human_data.RobotHumanData()
    print("action_is",decide_action_TATsys(robot_human_series_data))
