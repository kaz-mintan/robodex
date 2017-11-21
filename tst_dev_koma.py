# -*- coding: utf-8 -*-
#tst_dev.py cmd:sudo python3 tst_dev.py 

import wiringpi as pi
import time
import get_robo_actdata_led
import get_robo_actdata_motion

green_pin = 14
blue_pin = 15
red_pin = 23
servo_pin = 18

CYCLE = 20         # Unit : ms
SERVO_MIN = 0.5    # Unit : ms
SERVO_MAX = 2.4    # Unit : ms
RANGE = 180
clock = int( 19.2 / float(RANGE) * CYCLE * 1000 )
SERVO_MIN_VALUE = int( SERVO_MIN * RANGE / CYCLE )
SERVO_MAX_VALUE = int( SERVO_MAX * RANGE / CYCLE )

pi.wiringPiSetupGpio()
pi.pinMode( green_pin, pi.OUTPUT )
pi.pinMode( blue_pin, pi.OUTPUT )
pi.pinMode( red_pin, pi.OUTPUT )
pi.softPwmCreate( green_pin, 0, 100)
pi.softPwmCreate( blue_pin, 0, 100)
pi.softPwmCreate( red_pin, 0, 100)

pi.pinMode( servo_pin, pi.GPIO.PWM_OUTPUT )
pi.pwmSetMode( pi.GPIO.PWM_MODE_MS )
pi.pwmSetRange( RANGE )
pi.pwmSetClock( clock )

for num in range(1,4):


    ctlLED = get_robo_actdata_led.GetRobotActionDataOfLed()
    setLED = ctlLED.getRobotLed(num)

#komatsu
    if(0 != (len(setLED)-1)%10):
	print("テーブルの要素数に誤りあり。")
	#終了処理
    else:
        pass
    led_rep_maxnum = (len(setLED)-1)/10
	for led_rep_num in led_rep_maxnum:
	    pi.softPwmWrite( red_right_pin,  setLED[2+led_rep_num] )
            pi.softPwmWrite( green_right_pin, setLED[3+led_rep_num] )
            pi.softPwmWrite( blue_right_pin, setLED[4+led_rep_num] )
            pi.softPwmWrite( red_center_pin,  setLED[5+led_rep_num] )
            pi.softPwmWrite( green_center_pin, setLED[6+led_rep_num] )
            pi.softPwmWrite( blue_center_pin, setLED[7+led_rep_num] )
            pi.softPwmWrite( red_left_pin,  setLED[8+led_rep_num] )
            pi.softPwmWrite( green_left_pin, setLED[9+led_rep_num] )
            pi.softPwmWrite( blue_left_pin, setLED[10+led_rep_num] )
            time.sleep(setLED[1+led_rep_num] / 1000)

    pi.softPwmWrite( red_pin,  0 )
    pi.softPwmWrite( green_pin, 0 )
    pi.softPwmWrite( blue_pin, 0 )

    ctlSRV = get_robo_actdata_motion.GetRobotActionDataOfMotion()
    setSRV = ctlSRV.getRobotMotion(num)

    target = int( float( SERVO_MAX_VALUE - SERVO_MIN_VALUE ) / 180.0 * float( setSRV[1]  + 90 ) ) + SERVO_MIN_VALUE 
    print(target)
    pi.pwmWrite( servo_pin, target )
    time.sleep(setSRV[2]*2 / 1000)

    target = int( float( SERVO_MAX_VALUE - SERVO_MIN_VALUE ) / 180.0 * float( setSRV[3]  + 90 ) ) + SERVO_MIN_VALUE 
    print(target)
    pi.pwmWrite( servo_pin, target )
    time.sleep(setSRV[4]*2 / 1000)

    target = int( float( SERVO_MAX_VALUE - SERVO_MIN_VALUE ) / 180.0 * float( setSRV[5]  + 90 ) ) + SERVO_MIN_VALUE 
    print(target)
    pi.pwmWrite( servo_pin, target )
    time.sleep(setSRV[6]*2 / 1000)

time.sleep(1)
pi.pinMode( servo_pin, pi.OUTPUT )
