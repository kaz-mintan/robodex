# -*- coding: utf-8 -*-
#tst_dev.py cmd:sudo python3 tst_dev.py

import wiringpi as pi
import time
import get_robo_actdata_led
import get_robo_actdata_motion
import libokao

#以下、不要なものもあるはず。
import requests
import json
import os
import subprocess
#commandsは、python3ではsubprocessに内包された
#import commands
import get_robo_actdata_comment
import get_robo_actdata_motion
import get_robo_actdata_led
import tbl_robo_comment
import config

servo_pin = 18

blue_right_pin = 16
green_right_pin = 20
red_right_pin = 21

blue_left_pin = 25
green_left_pin = 8
red_left_pin = 7

blue_center_pin = 17
green_center_pin = 23
red_center_pin = 24

servo_pin = 18#raspPi 12pin

green_right_pin = 16#raspPi 36pin
blue_right_pin = 20#raspPi 38pin
red_right_pin = 21#raspPi 40pin

green_left_pin = 25#raspPi 22pin
blue_left_pin = 8#raspPi 24pin
red_left_pin = 7#raspPi 26pin

#blue_center_pin = 17
#green_center_pin = 23
#red_center_pin = 24

CYCLE = 20         # Unit : ms
SERVO_MIN = 0.5    # Unit : ms
SERVO_MAX = 2.4    # Unit : ms
RANGE = 180
clock = int( 19.2 / float(RANGE) * CYCLE * 1000 )
SERVO_MIN_VALUE = int( SERVO_MIN * RANGE / CYCLE )
SERVO_MAX_VALUE = int( SERVO_MAX * RANGE / CYCLE )

pi.wiringPiSetupGpio()
pi.pinMode( blue_right_pin, pi.OUTPUT )
pi.pinMode( green_right_pin, pi.OUTPUT )
pi.pinMode( red_right_pin, pi.OUTPUT )
pi.pinMode( blue_left_pin, pi.OUTPUT )
pi.pinMode( green_left_pin, pi.OUTPUT )
pi.pinMode( red_left_pin, pi.OUTPUT )

pi.pinMode( blue_center_pin, pi.OUTPUT )
pi.pinMode( green_center_pin, pi.OUTPUT )
pi.pinMode( red_center_pin, pi.OUTPUT )

pi.softPwmCreate( blue_right_pin, 0, 100)
pi.softPwmCreate( green_right_pin, 0, 100)
pi.softPwmCreate( red_right_pin, 0, 100)
pi.softPwmCreate( blue_left_pin, 0, 100)
pi.softPwmCreate( green_left_pin, 0, 100)
pi.softPwmCreate( red_left_pin, 0, 100)

pi.softPwmCreate( blue_center_pin, 0, 100)
pi.softPwmCreate( green_center_pin, 0, 100)
pi.softPwmCreate( red_center_pin, 0, 100)

pi.pinMode( servo_pin, pi.GPIO.PWM_OUTPUT )
pi.pwmSetMode( pi.GPIO.PWM_MODE_MS )
pi.pwmSetRange( RANGE )
pi.pwmSetClock( clock )

def execute_robot_action(robot_action):
    #robot_actionを通し番号として、テーブルに書かれた動作をする。
    #話す、首振り動作、LED点灯
    #上3つ、とりあえず順番に動かすようにしているが、並行して動かせるようにしないといけない。

    if robot_action == (0,0,0):
        return
    else:
        pass

    if 0 != robot_action[0]:#コメントアクションを行う。

        #テーブルファイルから取得するクラスを呼ぶ
        #speak_message = テーブルファイルから取得したメッセージ

#        if(50 == robot_motion[0]):

#        speak_message = '何か伺いましょうか？'
#        speak_message = tbl_robo_comment.list_robot_term[robot_action[0]][1]
        speak_message = tbl_robo_comment.dict_robot_term[robot_action[0]]

        check = subprocess.getoutput(config.VOICE_TEXT_SETTING % speak_message)
    else:
        pass

    if 0 != robot_action[2]:#LEDアクションを行う。
        ctlLED = get_robo_actdata_led.GetRobotActionDataOfLed()
        setLED = ctlLED.getRobotLed(robot_action[2])

    if 0 != robot_action[1]:#モーションを行う。

        ctlSRV = get_robo_actdata_motion.GetRobotActionDataOfMotion()
        setSRV = ctlSRV.getRobotMotion(robot_action[1])

        target = int( float( SERVO_MAX_VALUE - SERVO_MIN_VALUE ) / 180.0 * float( setSRV[1]  + 90 ) ) + SERVO_MIN_VALUE
    #    print(target)
        pi.pwmWrite( servo_pin, target )
        time.sleep(setSRV[2]*6 / 1000)

        target = int( float( SERVO_MAX_VALUE - SERVO_MIN_VALUE ) / 180.0 * float( setSRV[3]  + 90 ) ) + SERVO_MIN_VALUE
    #    print(target)
        pi.pwmWrite( servo_pin, target )
        time.sleep(setSRV[4]*6 / 1000)

        target = int( float( SERVO_MAX_VALUE - SERVO_MIN_VALUE ) / 180.0 * float( setSRV[5]  + 90 ) ) + SERVO_MIN_VALUE
    #    print(target)
        pi.pwmWrite( servo_pin, target )
        time.sleep(setSRV[6]*6 / 1000)
    else:
        pass

    if 0 != robot_action[2]:#LEDアクションを行う。
        ctlLED = get_robo_actdata_led.GetRobotActionDataOfLed()
        setLED = ctlLED.getRobotLed(robot_action[2])

        if(0 != (len(setLED)-1)%7):
            print("robot_action[2]="+robot_action[2])
            print("テーブルの要素数に誤りあり。")

        else:
            pass
        led_rep_maxnum = int((len(setLED)-1)/7)

        for led_rep_num in range(led_rep_maxnum):
            offset = led_rep_num * 7
            print('times:'+str(led_rep_num), 'offset:'+str(offset))
            pi.softPwmWrite( red_right_pin,  setLED[2+offset] )
            pi.softPwmWrite( green_right_pin, setLED[3+offset] )
            pi.softPwmWrite( blue_right_pin, setLED[4+offset] )
            pi.softPwmWrite( red_left_pin,  setLED[5+offset] )
            pi.softPwmWrite( green_left_pin, setLED[6+offset] )
            pi.softPwmWrite( blue_left_pin, setLED[7+offset] )
            time.sleep(setLED[1+offset] / 1000)

        pi.softPwmWrite( red_right_pin,  0 )
        pi.softPwmWrite( green_right_pin, 0 )
        pi.softPwmWrite( blue_right_pin, 0 )
        pi.softPwmWrite( red_left_pin,  0 )
        pi.softPwmWrite( green_left_pin, 0 )
        pi.softPwmWrite( blue_left_pin, 0 )

    else:
        pass

#---execute_robot_action確認用---
#robot_action = [1,0,0]
#execute_robot_action(robot_action)
