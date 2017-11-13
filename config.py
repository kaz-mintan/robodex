#config.py

#模擬的な定数（大文字、模擬的なのは、実際には変数なので）はここで定義する。
#グローバル変数（モジュール変数？）はここで定義する。

#他の全てのファイルで、
#import config　を記載する。
#参照する際は、例えば、以下のようにする。
#config.RESERVE_NUM_ROBOT_HUMAN_DATA


#最大で保存しておく、ロボットと人間の一連のやり取りデータの数
RESERVE_NUM_ROBOT_HUMAN_DATA = 10

#対話システムの選択スイッチ、まずは手動切り替えにする。
#0:ルールベースシステム　1:TAT学習システム
SW_DIALOGUE_SYS = 0

GOOGLE_APIKEY = 'AIzaSyDSC8btGZn8HsbiP9Fz3t53XzVxJDK9fs0'
#GOOGLE_APIKEY = 'AIzaSyDXPTSsgQQSEsRwsrMX9cWmUZiAmppLqyY'
#GOOGLE_APIKEY = 'AIzaSyCBYnDP4ZRzB1U6YAXm6o0KRA7rV-ETJWE'

VOICE_REC_PATH = '/home/pi/robodex/human_comment.wav'

#VOICETEXTのKEYも、本来ここに書いておきたい
