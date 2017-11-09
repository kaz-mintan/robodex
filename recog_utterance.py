# -*- coding: utf-8 -*-
#recog_utterance.py

#以下、不要なものもあるはず。
import requests
import json
import os
import time
import subprocess
import commands
import config.py

def current_milli_time():
    return int(round(time.time() * 1000))

def recognize_utterance():

    print('recognizing...')
    f = open(VOICE_REC_PATH, 'rb')
    print('recognizing...1')
    voice = f.read()
    print('recognizing...2')
    f.close()
    print('recognizing...3')

    url = 'https://www.google.com/speech-api/v2/recognize?xjerr=1&client=chromium&'\
        'lang=ja-JP&maxresults=10&pfilter=0&xjerr=1&key=' + GOOGLE_APIKEY

    print('recognizing...4')
    hds = {'Content-type': 'audio/l16; rate=16000;'}

    print('recognizing...5')
    try:
        print('recognizing...51')
        reply = requests.post(url, data=voice, headers=hds).text
        print (reply)
    except IOError:
        print('recognizing...52')
        return '#CONN_ERR'
    except:
        print('recognizing...53')
        return '#ERROR'

    print('recognizing...6')

    print 'results:', reply

    objs = reply.split(os.linesep)
    for obj in objs:
        if not obj:
            continue
        alternatives = json.loads(obj)['result']

        if len(alternatives) == 0:
            continue
        return alternatives[0]['alternative'][0]['transcript']
    return ""

    print('recognizing...7')

#上までは1回やればいい？
    cmd = "rec --encoding signed-integer --bits 16 --channels 1 --rate 16000 human_comment.wav trim 0 3"
    subprocess.call( cmd.strip().split(" ")  )

    t0 = current_milli_time()
    message = recognize().encode('utf-8')
    print 'recognized:' + str(current_milli_time() - t0) + 'ms'

    if (message == '#CONN_ERR'):
        print 'internet not available'
        message = ''
    elif (message == '#ERROR'):
        print 'voice recognizing failed'
        message = ''
    else:
        print 'your words:' + message

recognize_utterance()
