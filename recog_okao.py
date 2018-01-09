# -*- coding: utf-8 -*-
#recog_okao.py

import time#debug用
import concurrent.futures#debug用

import libokao
import robo_human_data

okao_data = [[]]

def recognize_okao():
    libokao.okao_init(0,9600)

    while True:
#    for var in range(0, 15):
        libokao.okao_exec()

        #取得の順番は、年齢、性別、驚、怒、哀、楽、ニュートラル（喜怒哀楽ではなく、驚、怒、哀、楽、ニュートラル）
        okao_data.insert(0,([
        libokao.okao_getAge(),
        libokao.okao_getGender(),

        libokao.okao_getSurprise(),
        libokao.okao_getAnger(),
        libokao.okao_getSadness(),
        libokao.okao_getHappiness(),
        libokao.okao_getNeutral()
        ]))

        #取得の順番は、年齢、性別、驚、怒、哀、楽、ニュートラル（喜怒哀楽ではなく、驚、怒、哀、楽、ニュートラル）
        print("okao age            :",okao_data[0][0])
        print("okao gendre(1:m,2:f):",okao_data[0][1])
        print("okao surprise(%) :",okao_data[0][2])
        print("okao anger(%)    :",okao_data[0][3])
        print("okao sadness(%)  :",okao_data[0][4])
        print("okao happiness(%):",okao_data[0][5])
        print("okao neutral(%)  :",okao_data[0][6])

        if len(okao_data) > 10:
            okao_data.pop()

        time.sleep(2)#1秒以下にすると、他のスレッドの回りが悪くなる
    libokao.okao_close()
