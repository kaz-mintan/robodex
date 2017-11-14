# -*- coding: utf-8 -*-
#tbl_human_comment.py

#辞書ファイルかリストかタプルとして書いておく
#csvやtxtで書いてあるのを読み込むのが難しそうだから
#行によって、要素数が異なることに対応しないといけない
#検索方法を考えないといけない
#もしかしたら、検索時間も考慮しないといけない
#JSONとかでできる？

#ここに書かれている、全要素、例えば、（こんにちは、コンニチワ）、（いい、よい、良い）、など全てを１行ずつ、
#認識結果（例えば、「こんにちは、いい天気だなー」）に対して検索していく必要がある。
#この場合は、"こんにちは"と、"いい"が検索で見つかるべきで、
#その見出しの、"konnichiha"と、"ii"が検索結果となるべき。

#0,konnichiha,こんにちは,コンニチワ
#1,tsukareta,疲れた,ツカレタ
#2,yoi,いい,よい,良い

dict = {

    "こんにちは":("こんにちは",),
    "疲れた":("疲れた","つかれた"),
    "良い":("いい","よい","良い")

}

pic_term_list = []

msg = "良いけど疲れた。"

for key in dict:

    list = dict[key]

    for number in range(len(list)):
#        print (list[number])
        if msg.find(list[number]) > -1:
#        if True == list[number] in msg:　これだとうまくいかない
#            print(msg.find(list[number]))
            pic_term_list.append(key)
            break
        else:
            pass

for number in range(len(pic_term_list)):
    print (pic_term_list[number])
