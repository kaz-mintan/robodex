import time
import concurrent.futures
import robo_human_data
import recog_okao

def get_okao_data_test():
#    data = [[]]
    tmp = robo_human_data.RobotHumanData()
    while True:
        time.sleep(1)
        tmp.setOkaoVisionData()
        data = tmp.getOkaoVisionData()
#        print("get_okao_data_test",data)

if __name__ == '__main__':
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(recog_okao.recognize_okao)
    executor.submit(get_okao_data_test)
