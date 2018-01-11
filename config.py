# -*- coding: utf-8 -*-
#config.py

#模擬的な定数（大文字、模擬的なのは、実際には変数なので）はここで定義する。
#グローバル変数（モジュール変数？）はここで定義する。

# 最大で保存しておく、ロボットと人間の一連のやり取りデータの数
RESERVE_NUM_ROBOT_HUMAN_DATA = 10  # ここの数値変更したら、decide_action_rulebaseでも変更する必要になる部分あり。

# 対話システムの選択スイッチ、まずは手動切り替えにする。
# 0:ルールベースシステム　1:TAT学習システム
SW_DIALOGUE_SYS = 1

VOICE_TEXT_SETTING = 'curl "https://api.voicetext.jp/v1/tts" -s -u 563fw3j9tnberqyq: -d speed=135 -d speaker=santa -d "text=%s" | aplay 2> /dev/null '

VOICE_REC_PATH = 'human_comment.wav'
VOICE_RECORD_SECONDS = 2.5

DEBUG_PRINT = 1 #0:通常動作 1:debugモード、debug用にprintする
#koko

DEBUG_MODE0 = 0 #0:通常動作 1:debugモード
# 1の時
# mainでの繰り返しをしない。end_flagを強制でTrueにする。

NUM_OF_CHOICES_MOTION = 1
NUM_OF_CHOICES_LED = 7

OKAO_EXEC_CYCLE_SEC = 2
MAX_MULTI_EXECUTE_WORKERS_NO = 4

TAT_REWARD_TBL = 'tat_reward_tbl.csv'

def debug_print(debug_comment):
    if 1 == DEBUG_PRINT:
        print(debug_comment)
