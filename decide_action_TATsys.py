# coding:utf-8
#decide_action_TATsys.py
#関数よりクラスの方が良いのかな？
import numpy as np
from numpy.random import *
import itertools

#import tbl_robo_comment
#import tbl_robo_led
#import tbl_robo_motion

import robo_human_data

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

def decide_action_TATsys(robot_human_series_data):
    action_candidate = robo_human_data.RobotHumanData()

    #TODO: get the possible range from the tbl?
    possible_range_comment=3
    possible_range_motion=4
    possible_range_led=5

    possible_list=[range(possible_range_comment),
            range(possible_range_motion),
            range(possible_range_led)]

    prediction=np.zeros((possible_range_comment,possible_range_motion,possible_range_led))
    reward=np.zeros((possible_range_comment,possible_range_motion,possible_range_led))

    for (i, j, k) in itertools.product(range(possible_range_comment),
            range(possible_range_motion),
            range(possible_range_led)):
        action_candidate.robot_comment=i
        action_candidate.robot_motion=j
        action_candidate.robot_led=k

        reward[i,j,k]=calc_reward(face_predict(robot_human_series_data,action_candidate))
        print(i,j,k,reward[i,j,k])

    #argmax
    robot_action = argmax_ndim(reward)
    #print(robot_action)

    #TATシステムでhogehogeする

    return robot_action

if __name__ == "__main__" :
    robot_human_series_data = robo_human_data.RobotHumanData()
    print("action_is",decide_action_TATsys(robot_human_series_data))
