#from xml.dom import minicompat
import numpy as np
#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
#import time
#import schedule

import sys, pprint
print(sys.path)

# ヘッドレスモードの場合コメントイン
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
def randomize_time() -> list[str]:
    """
    1日4回（）打刻するため、打刻時間をランダムに決める。
    昼休みはぴったり1時間とする。

    Returns:
        list[str]: 打刻する時間（出勤時、昼休み開始時間、昼休み終了時間の終業時の4回）
    """

    list_hours = [9, 12, 13, 18]
    list_hhmmss = []

    # 時間（分、秒）をランダムにする。
    for i, hour  in enumerate(list_hours):
        if hour == 13:
            minutes = list_hhmmss[i-1][3:5]
            print(minutes)
            seconds = str(int(round(np.random.rand()*60, 0)))
            list_hhmmss.append(f'{str(hour)}:{str(minutes)}:{str(seconds)}')
        
        else:
            minutes, seconds = str(int(np.random.uniform(0,59))), str(int(np.random.uniform(0,59)))
            list_hhmmss.append(f'{str(hour)}:{str(minutes)}:{str(seconds)}')

    return list_hhmmss

def stamp(time):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #　 ヘッドレスモードの場合
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    driver.find_element_by_name('UserID').send_keys(id)
    driver.find_element_by_name('_word').send_keys(password)
    driver.find_element_by_id("login-btn").click()
    time.sleep(1)
    driver.find_element_by_xpath("//li[@title='タイムカード']").click()
    time.sleep(1)

    if time == '8:00':
        driver.find_element_by_class_name('jtcard-btn-stime').click()
    elif time == '12:00':
        driver.find_element_by_class_name('jtcard-btn-outtime').click()
    elif time == '12:50':
        driver.find_element_by_class_name('jtcard-btn-intime').click()
    elif time == '18:00':
        driver.find_element_by_class_name('jtcard-btn-etime').click()
    driver.quit()

# 平日の8時45分、12時、12時50分、18時に打刻
for i in ["08:45", "12:00", "12:50", "18:00"]:
    schedule.every().monday.at(i).do(stamp)
    schedule.every().tuesday.at(i).do(stamp)
    schedule.every().wednesday.at(i).do(stamp)
    schedule.every().thursday.at(i).do(stamp)
    schedule.every().friday.at(i).do(stamp)

# 指定時間になったらstamp関数を実行
while True:
    schedule.run_pending()
    time.sleep(1)

print(randomize_time())



