# -*- coding: utf-8 -*-
#tst_dev.py cmd:sudo python3 tst_dev.py
#ラズパイIOからLED・電源基板へのgreenとblueの線を左右分ともテレコにしている

import wiringpi as pi
import time
import get_robo_actdata_led
import get_robo_actdata_motion
import libokao

servo_pin = 18#raspPi 12pin

right_eye_red_pin = 16#raspPi 36pin
right_eye_green_pin = 20#raspPi 38pin
right_eye_blue_pin = 21#raspPi 40pin

left_eye_red_pin = 25#raspPi 22pin
left_eye_green_pin = 8#raspPi 24pin
left_eye_blue_pin = 7#raspPi 26pin

CYCLE = 20         # Unit : ms
SERVO_MIN = 0.5    # Unit : ms
SERVO_MAX = 2.4    # Unit : ms
RANGE = 180
clock = int( 19.2 / float(RANGE) * CYCLE * 1000 )
SERVO_MIN_VALUE = int( SERVO_MIN * RANGE / CYCLE )
SERVO_MAX_VALUE = int( SERVO_MAX * RANGE / CYCLE )

pi.wiringPiSetupGpio()
pi.pinMode( right_eye_red_pin, pi.OUTPUT )
pi.pinMode( right_eye_green_pin, pi.OUTPUT )
pi.pinMode( right_eye_blue_pin, pi.OUTPUT )
pi.pinMode( left_eye_red_pin, pi.OUTPUT )
pi.pinMode( left_eye_green_pin, pi.OUTPUT )
pi.pinMode( left_eye_blue_pin, pi.OUTPUT )

pi.softPwmCreate( right_eye_red_pin, 0, 100)
pi.softPwmCreate( right_eye_green_pin, 0, 100)
pi.softPwmCreate( right_eye_blue_pin, 0, 100)
pi.softPwmCreate( left_eye_red_pin, 0, 100)
pi.softPwmCreate( left_eye_green_pin, 0, 100)
pi.softPwmCreate( left_eye_blue_pin, 0, 100)

pi.pinMode( servo_pin, pi.GPIO.PWM_OUTPUT )
pi.pwmSetMode( pi.GPIO.PWM_MODE_MS )
pi.pwmSetRange( RANGE )
pi.pwmSetClock( clock )

robot_action = [1,1,7]

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
        pi.softPwmWrite( right_eye_red_pin,  setLED[2+offset] )
        pi.softPwmWrite( right_eye_green_pin, setLED[3+offset] )
        pi.softPwmWrite( right_eye_blue_pin, setLED[4+offset] )
        pi.softPwmWrite( left_eye_red_pin,  setLED[5+offset] )
        pi.softPwmWrite( left_eye_green_pin, setLED[6+offset] )
        pi.softPwmWrite( left_eye_blue_pin, setLED[7+offset] )
        time.sleep(setLED[1+offset] / 1000)

    pi.softPwmWrite( right_eye_red_pin,  0 )
    pi.softPwmWrite( right_eye_green_pin, 0 )
    pi.softPwmWrite( right_eye_blue_pin, 0 )
    pi.softPwmWrite( left_eye_red_pin,  0 )
    pi.softPwmWrite( left_eye_green_pin, 0 )
    pi.softPwmWrite( left_eye_blue_pin, 0 )

else:
    pass


libokao.okao_init(0,9600)

libokao.okao_exec()

print(libokao.okao_getNeutral())
print(libokao.okao_getHappiness())
print(libokao.okao_getSurprise())
print(libokao.okao_getAnger())
print(libokao.okao_getSadness())
print(libokao.okao_getAge())
print(libokao.okao_getGender())

libokao.okao_exec()

print(libokao.okao_getNeutral())
print(libokao.okao_getHappiness())
print(libokao.okao_getSurprise())
print(libokao.okao_getAnger())
print(libokao.okao_getSadness())
print(libokao.okao_getAge())
print(libokao.okao_getGender())

libokao.okao_close()
