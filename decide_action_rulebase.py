#coding: UTF-8
#decide_action_rulebase.py
#関数よりクラスの方が良いのかな？

def decide_action_rulebase(robot_human_series_data)

    robot_action = (0,0,0)#ロボットのコメント、モーション、LEDの、それぞれのテーブルのID

    #rulebaseシステムでhogehogeする
    robot_human_data_newest = robot_human_series_data[0]
    tmp_human_comment = robot_human_data_newest.getHumanComment()

    
テーブルを2つ参照する必要がある？


#コメント表、アクション表からどう取得するかを考える必要あり。

    return robot_action





#以下、メモ。最後消す
'''
mydict = []{}
mydict[0] = {"apple":1, "orange":2, "banana":3}
val = mydict[0]["apple"]
print(val)
'''
'''
dict = {"itou":64, "yamada":75, "endou":82}
print dict["itou"]
print dict["yamada"]
print dict["endou"]
'''
