# -*- coding: utf-8 -*-
#tst_dev.py cmd:sudo python3 tst_dev.py 

import wiringpi as pi
import time
import get_robo_actdata_led
import get_robo_actdata_motion

servo_pin = 18

blue_right_pin = 15
green_right_pin = 23
red_right_pin = 24

blue_left_pin = 25
green_left_pin = 8
red_left_pin = 7

blue_center_pin = 16
green_center_pin = 20
red_center_pin = 21

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

for num in range(1,4):
    ctlLED = get_robo_actdata_led.GetRobotActionDataOfLed()
    setLED = ctlLED.getRobotLed(num)

    print('num' + str(num))
    if(0 != (len(setLED)-1)%10):
        print("テーブルの要素数に誤りあり。")
        break
    else:
        pass
    led_rep_maxnum = int((len(setLED)-1)/10)

    for led_rep_num in range(led_rep_maxnum):
        offset = led_rep_num * 10
        print('times:'+str(led_rep_num), 'offset:'+str(offset))
        pi.softPwmWrite( red_right_pin,  setLED[2+offset] )
        pi.softPwmWrite( green_right_pin, setLED[3+offset] )
        pi.softPwmWrite( blue_right_pin, setLED[4+offset] )
        pi.softPwmWrite( red_center_pin,  setLED[5+offset] )
        pi.softPwmWrite( green_center_pin, setLED[6+offset] )
        pi.softPwmWrite( blue_center_pin, setLED[7+offset] )
        pi.softPwmWrite( red_left_pin,  setLED[8+offset] )
        pi.softPwmWrite( green_left_pin, setLED[9+offset] )
        pi.softPwmWrite( blue_left_pin, setLED[10+offset] )
        time.sleep(setLED[1+offset] / 1000)    

    pi.softPwmWrite( red_right_pin,  0 )
    pi.softPwmWrite( green_right_pin, 0 )
    pi.softPwmWrite( blue_right_pin, 0 )
    pi.softPwmWrite( red_center_pin,  0 )
    pi.softPwmWrite( green_center_pin, 0 )
    pi.softPwmWrite( blue_center_pin, 0 )
    pi.softPwmWrite( red_left_pin,  0 )
    pi.softPwmWrite( green_left_pin, 0 )
    pi.softPwmWrite( blue_left_pin, 0 )


    ctlSRV = get_robo_actdata_motion.GetRobotActionDataOfMotion()
    setSRV = ctlSRV.getRobotMotion(num)

    target = int( float( SERVO_MAX_VALUE - SERVO_MIN_VALUE ) / 180.0 * float( setSRV[1]  + 90 ) ) + SERVO_MIN_VALUE 
#    print(target)
    pi.pwmWrite( servo_pin, target )
    time.sleep(setSRV[2]*2 / 1000)

    target = int( float( SERVO_MAX_VALUE - SERVO_MIN_VALUE ) / 180.0 * float( setSRV[3]  + 90 ) ) + SERVO_MIN_VALUE 
#    print(target)
    pi.pwmWrite( servo_pin, target )
    time.sleep(setSRV[4]*2 / 1000)

    target = int( float( SERVO_MAX_VALUE - SERVO_MIN_VALUE ) / 180.0 * float( setSRV[5]  + 90 ) ) + SERVO_MIN_VALUE 
#    print(target)
    pi.pwmWrite( servo_pin, target )
    time.sleep(setSRV[6]*2 / 1000)
