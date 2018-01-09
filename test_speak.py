# -*- coding: utf-8 -*-
import subprocess
import config

speak_message = "これは、テストテストです。"
subprocess.getoutput(config.VOICE_TEXT_SETTING % speak_message)
config.debug_print("実行完了")
