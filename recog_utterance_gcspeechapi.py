# -*- coding: utf-8 -*-
#recog_utterance.py

#以下、不要なものもあるはず。
import requests
import json
import os
import time
import subprocess
#commandsは、python3ではsubprocessに内包された
import config

#import exe_robo_action as pin
#import wiringpi as pi

#下記、config.pyへの記載ではダメなのかな？
#VOICE_REC_PATH = '/home/pi/robodex/human_comment.wav'
#GOOGLE_APIKEY = 'AIzaSyDSC8btGZn8HsbiP9Fz3t53XzVxJDK9fs0'

def execute_recognition():
#    if 1 == config.DEBUG_PRINT:print('recognizing...')
#    f = open(config.VOICE_REC_PATH, 'rb')
#    if 1 == config.DEBUG_PRINT:print('recognizing...1')
#    voice = f.read()
#    if 1 == config.DEBUG_PRINT:print('recognizing...2')
#    f.close()
#    if 1 == config.DEBUG_PRINT:print('recognizing...3')

#    url = 'https://www.google.com/speech-api/v2/recognize?xjerr=1&client=chromium&'\
#        'lang=ja-JP&maxresults=10&pfilter=0&xjerr=1&key=' + config.GOOGLE_APIKEY

    if 1 == config.DEBUG_PRINT:print('recognizing...4')
#    hds = {'Content-type': 'audio/l16; rate=16000;'}
    hds = {
        "Accept": "application/json",
        "Content-type": "application/json"
    }
    data = {
        "config": {
            "encoding": "FLAC",
            "sampleRateHertz": 16000,
            "languageCode": "en-US"
        },
        "audio": {
            "uri": "gs://cloud-samples-tests/speech/brooklyn.flac"
        }
    }


    if 1 == config.DEBUG_PRINT:print('recognizing...5')
    try:
        if 1 == config.DEBUG_PRINT:print('recognizing...51')

        reply = requests.post("https://speech.googleapis.com/v1/speech:recognize?key= AIzaSyDSC8btGZn8HsbiP9Fz3t53XzVxJDK9fs0",
            data=json.dumps(data),
            headers=hds).text

#        reply = requests.post(url, data=voice, headers=hds).text
#        print (reply)
    except IOError:
        if 1 == config.DEBUG_PRINT:print('recognizing...52')
        return '#CONN_ERR'
    except Exception as err:
        print(err)
        if 1 == config.DEBUG_PRINT:print('recognizing...53')
        return '#ERROR'

    if 1 == config.DEBUG_PRINT:print('recognizing...6')

    print('results:', reply)

#    objs = reply.split(os.linesep)
#    for obj in objs:
#        if not obj:
#            continue
#        alternatives = json.loads(obj)['result']
#
#        if len(alternatives) == 0:
#            continue
#    return ""
#    print('recognizing...7')

def current_milli_time():
    return int(round(time.time() * 1000))

#上までは1回やればいい？
def recognize_utterance():
    #下記ディレクトリ指定は、本来configファイルで行う。

#    pi.softPwmWrite( pin.right_eye_green_pin, 100)
#    pi.softPwmWrite( pin.left_eye_green_pin, 100)

#    cmd = "rec --encoding signed-integer --bits 16 --channels 1 --rate 16000 human_comment.wav trim 0 2.5"
#    subprocess.call( cmd.strip().split(" ")  )

#    pi.softPwmWrite( pin.right_eye_green_pin, 0)
#    pi.softPwmWrite( pin.left_eye_green_pin, 0)

#    t0 = current_milli_time()
#    message = execute_recognition().encode('utf-8')#python2
    message = execute_recognition()

#    print('recognized:' + str(current_milli_time() - t0) + 'ms')

    if (message == '#CONN_ERR'):
        print('internet not available')
        message = ''
    elif (message == '#ERROR'):
        print('voice recognizing failed')
        message = ''
    else:
        print('your words:' + str(message))#python2?
#        print('your words:' + message)

    if 1 == config.DEBUG_PRINT:
        print("message = ")
        print(message)
        print("str message = ")
        print(str(message))

    return message

if __name__ == '__main__':
#    recognize_utterance()
    message = recognize_utterance()
