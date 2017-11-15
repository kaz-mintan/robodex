# -*- coding: utf-8 -*-
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

def execute_robot_action(robot_action):
    #robot_actionを通し番号として、テーブルに書かれた動作をする。
    #話す、首振り動作、LED点灯
    #上3つ、とりあえず順番に動かすようにしているが、並行して動かせるようにしないといけない。

    if robot_action == (0,0,0):
        pass

    elif 0 != robot_action[0]:#コメントアクションを行う。

        #テーブルファイルから取得するクラスを呼ぶ
        #speak_message = テーブルファイルから取得したメッセージ

        #speak_message = '何か伺いましょうか？'
        check = subprocess.getoutput('curl "https://api.voicetext.jp/v1/tts" -s -u 563fw3j9tnberqyq: -d speed=100 -d speaker=hikari -d "text=%s" | aplay 2> /dev/null '% speak_message)

    elif 0 != robot_action[1]:#モーションを行う。
        #テーブルファイルから取得するクラスを呼ぶ
        pass
    elif 0 != robot_action[2]:#LEDアクションを行う。
        #テーブルファイルから取得するクラスを呼ぶ
        pass
    else:
        pass

#---execute_robot_action確認用---
#robot_action = [0,0,0]
#execute_robot_action(robot_action)
