# -*- coding: utf-8 -*-
#recog_utterance.py

#以下、不要なものもあるはず。
import requests
import json
import time
import subprocess
#commandsは、python3ではsubprocessに内包された
import config as conf
import apikey
import base64

import exe_robo_action as pin
import wiringpi as pi

def execute_recognition():
    audio = open(conf.VOICE_REC_PATH,'rb')
    audio_content = audio.read()
    audio_encode_file = base64.b64encode(audio_content)
    audio_encode_file_dec = audio_encode_file.decode("utf-8")

    conf.debug_print('recognizing...4')
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
            "content": audio_encode_file_dec
        }
    }

    conf.debug_print('recognizing...5')
    try:
        conf.debug_print('recognizing...51')

        reply = requests.post("https://speech.googleapis.com/v1/speech:recognize?key="+ apikey.GOOGLE_APIKEY,
            data = json.dumps(data),
            headers = hds).text

    except IOError:
        conf.debug_print('recognizing...52')
        return '#CONN_ERR'
    except Exception as err:
        print(err)
        conf.debug_print('recognizing...53')
        return '#ERROR'

    conf.debug_print('recognizing....6')

    conf.debug_print('reply: '+str(reply))

    reply_json = json.loads(reply)
    conf.debug_print('reply_json: '+str(reply_json))

    results = reply_json.get('results',"")
    if not ("" == results):
        transcript = results[0]['alternatives'][0].get('transcript')
    else:
        transcript = ""
#以下のように書くと、無言の録音データの場合に、KeyError: 'results'が出る。
#    transcript = reply_json['results'][0]['alternatives'][0]['transcript']
    conf.debug_print('transcript: '+str(transcript))

    return transcript

def current_milli_time():
    return int(round(time.time() * 1000))

def recognize_utterance():

    pi.softPwmWrite( pin.right_eye_green_pin, 100)
    pi.softPwmWrite( pin.left_eye_green_pin, 100)

    cmd = ("rec --encoding signed-integer --bits 16 --channels 1 --rate 16000 %s trim 0 %f"%(conf.VOICE_REC_PATH,conf.VOICE_RECORD_SECONDS))
    subprocess.call( cmd.strip().split(" ")  )

    pi.softPwmWrite( pin.right_eye_green_pin, 0)
    pi.softPwmWrite( pin.left_eye_green_pin, 0)

    t0 = current_milli_time()
    message = execute_recognition()

    print('recognized:' + str(current_milli_time() - t0) + 'ms')

    if (message == '#CONN_ERR'):
        print('internet not available')
        message = ''
    elif (message == '#ERROR'):
        print('voice recognizing failed')
        message = ''
    else:
        print('your words:' + message)

    conf.debug_print("message: "+str(message))

    return message

if __name__ == '__main__':
    message = recognize_utterance()
