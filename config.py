#config.py

#模擬的な定数（大文字、模擬的なのは、実際には変数なので）はここで定義する。
#グローバル変数（モジュール変数？）はここで定義する。

#他の全てのファイルで、
#import config　を記載する。
#参照する際は、例えば、以下のようにする。
#config.RESERVE_NUM_ROBOT_HUMAN_DATA


#最大で保存しておく、ロボットと人間の一連のやり取りデータの数
RESERVE_NUM_ROBOT_HUMAN_DATA = 10#ここの数値変更したら、decide_action_rulebaseでも変更する必要になる部分あり。

#対話システムの選択スイッチ、まずは手動切り替えにする。
#0:ルールベースシステム　1:TAT学習システム
SW_DIALOGUE_SYS = 0

GOOGLE_APIKEY = 'AIzaSyDSC8btGZn8HsbiP9Fz3t53XzVxJDK9fs0'
#GOOGLE_APIKEY = 'AIzaSyDXPTSsgQQSEsRwsrMX9cWmUZiAmppLqyY'
#GOOGLE_APIKEY = 'AIzaSyCBYnDP4ZRzB1U6YAXm6o0KRA7rV-ETJWE'

VOICE_TEXT_SETTING = 'curl "https://api.voicetext.jp/v1/tts" -s -u 563fw3j9tnberqyq: -d speed=135 -d speaker=santa -d "text=%s" | aplay 2> /dev/null '

VOICE_REC_PATH = '/home/pi/robodex/human_comment.wav'

DEBUG_PRINT = 1 #0:通常動作 1:debugモード、debug用にprintする

DEBUG_MODE0 = 0 #0:通常動作 1:debugモード
#1の時
#mainでの繰り返しをしない。end_flagを強制でTrueにする。

#VOICETEXTのKEYも、本来ここに書いておきたい

NUM_OF_CHOICES_MOTION = 1

NUM_OF_CHOICES_LED = 7
