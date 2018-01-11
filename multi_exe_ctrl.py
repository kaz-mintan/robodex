import concurrent.futures
import config

executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.MAX_MULTI_EXECUTE_WORKERS_NO)
#    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)#認識中のLED光らない
