
#VOICE TEXT APIの設定
#https://cloud.voicetext.jp/webapi/docs/api

import subprocess

ALSA_SPEAKER_DVICE = "PCM"#amixerコマンドで確認できる。Simple mixer control 'PCM',0
alsa_volume = 70#0-100

VOICE_TEXT_URL = "https://api.voicetext.jp/v1/tts"
VOICE_TEXT_OUTPUT_FILE = "robot_comment.wav"
VOICE_TEXT_KEY = "563fw3j9tnberqyq:"

VOICE_TEXT_SPEAKER = "santa"#"show","haruka","hikari","takeru","santa","bear"

robot_comment = "なまむぎ、生米、生卵。あかまきがみ、あおまきがみ、きまきがみ。隣の客はよく柿食う客だ。"
voice_text_speed = 135#50-400 default: 100
voice_text_emotion = "happiness"#"", "happiness", "anger", "sadness"(このパラメータは、haruka、hikari、takeru、santa、bearにのみ使用可。showには使えない)
voice_text_emotion_level = 3#1-4 default: 2
voice_text_pitch = 100#50-200 default: 100
voice_text_volume = 200#50-200 default: 100
voice_text_emotion_setting = ""#初期値

#voice_text_emotion_settingの設定、感情設定をしない時に、APIに渡す該当引数を書かないように。
if not(("haruka"==VOICE_TEXT_SPEAKER)or("hikari"==VOICE_TEXT_SPEAKER)or("takeru"==VOICE_TEXT_SPEAKER)or("santa"==VOICE_TEXT_SPEAKER)or("bear"==VOICE_TEXT_SPEAKER)):
    voice_text_emotion_setting = ""
elif("" == voice_text_emotion):
    voice_text_emotion_setting = ""
elif("happiness" == voice_text_emotion)or("anger" == voice_text_emotion)or("sadness" == voice_text_emotion):
    voice_text_emotion_setting = ("emotion="+ voice_text_emotion)
else:
    print("error: voice_text_emotion_setting")

subprocess.getoutput('curl %s -o %s -u %s -d text=%s -d speaker=%s -d %s -d emotion_level=%d -d pitch=%d -d speed=%d -d volume=%d'%(VOICE_TEXT_URL, VOICE_TEXT_OUTPUT_FILE, VOICE_TEXT_KEY, robot_comment, VOICE_TEXT_SPEAKER, voice_text_emotion_setting, voice_text_emotion_level, voice_text_pitch, voice_text_speed, voice_text_volume))
subprocess.call(["amixer", "set", ALSA_SPEAKER_DVICE, str(alsa_volume)+"%"])
subprocess.call(["aplay", "./robot_comment.wav"])
