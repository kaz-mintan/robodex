# -*- coding: utf-8 -*-
#tbl_robo_led.csv
#フルカラーLEDを暫定3つ取り付ける→2つに変更
#1つのLEDで、各色0から100で設定できる

#7個のデータで1セットとする　点灯時間(ms)、向かって右目（向かって左LED）のRGB、左目（向かって右LED）のRGB
#10個のデータで1セットとする　点灯時間(ms)、向かって右LEDのRGB、中央LEDのRGB、左LEDのRGB

#.pyにして、ここでタプルを定義した方が良さそう。
#まずは固定長で考える。(id+n*(時間+RGB*3の10数字))
#つまり、要素数は、11 or 21 or 31 or...

class tblRobotLED:
    def __init__(self):
        self.DATA = [
            [0,   0,  0,  0,  0,  0,  0,  0],   #初期値
            [1,2000,100,100,100,100,100,100],   #2秒点灯
            [2,2000,100,0,0,100,0,0],   #2秒両目赤(R)
            [3,2000,0,100,0,0,100,0],   #2秒両目緑(G)
            [4,2000,0,0,100,0,0,100],   #2秒両目青(B)
            [5,1000,100,100,100,100,100,100],   #3秒点灯
            [6,1000,100,100,100,100,100,100,1000,0,0,0,0,0,0,1000,100,100,100,100,100,100],    #1秒インターバルの点滅
            [7,1000,100,0,0,0,0,100,1000,0,100,0,100,0,0,1000,0,0,100,0,100,0]  #1秒毎に色を変えていく（右目赤、左目青からスタート）
#            [0,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0],   #初期値
#            [1,3000,100,  0,  0,  0,100,  0,  0,  0,100],   #3秒点灯
#            [2,1000,100,100,100,100,100,100,100,100,100,1000,0,0,0,0,0,0,0,0,0,1000,100,100,100,100,100,100,100,100,100],    #1秒インターバルの点滅
#            [3,1000,100,0,0,0,100,0,0,0,100,1000,0,100,0,0,0,100,100,0,0,1000,0,0,100,100,0,0,0,100,0]  #1秒毎に色を変えていく
        ]
