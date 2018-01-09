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
import apikey
import base64

#import exe_robo_action as pin
#import wiringpi as pi

def execute_recognition():
    audio = open('/home/pi/robodex/human_comment.wav')
    audio_content = audio.read()
    print("type(audio_content): ",type(audio_content))
    audio_encode_file = base64.b64encode(audio_content)
    print("type(audio_encode_file): ",type(audio_encode_file))

#    audio_encode_file = str(audio_encode_file)

#    print("audio_encode_file: ",audio_encode_file)

    if 1 == config.DEBUG_PRINT:print('recognizing...4')
    hds = {
        "Accept": "application/json",
        "Content-type": "application/json"
    }
    data = {
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": 16000,
            "languageCode": "ja-JP"
        },
        "audio": {
            "content": audio_encode_file
        }
    }

    if 1 == config.DEBUG_PRINT:print('recognizing...5')
    try:
        if 1 == config.DEBUG_PRINT:print('recognizing...51')

        reply = requests.post("https://speech.googleapis.com/v1/speech:recognize?key="+ apikey.GOOGLE_APIKEY,
            data = json.dumps(data),
            headers = hds).text

    except IOError:
        if 1 == config.DEBUG_PRINT:print('recognizing...52')
        return '#CONN_ERR'
    except Exception as err:
        print(err)
        if 1 == config.DEBUG_PRINT:print('recognizing...53')
        return '#ERROR'

    if 1 == config.DEBUG_PRINT:print('recognizing...6')

    print('results:', reply)
#    print('results:', reply.encode('utf-8'))  # python2???

    reply_json = json.loads(reply)
    print("type(reply_json): ",type(reply_json))
    print(reply_json)

    transcript = reply_json['results'][0]['alternatives'][0]['transcript']
    print(transcript)

    return transcript

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
#        print('your words:' + str(message))#python2?
        print('your words:' + message)

    if 1 == config.DEBUG_PRINT:
        print("message: ", message)
#        print("str message = ")
#        print(str(message))

    return message

if __name__ == '__main__':
#    recognize_utterance()
    message = recognize_utterance()
    print("message: ",message)
