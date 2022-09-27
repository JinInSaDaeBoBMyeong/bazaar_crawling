import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unzip
import md5
import pymysql



def crawling():
    #my sql 연결
    conn = pymysql.connect(host='localhost', user = 'root', password='데베 비번',db = 'malware_apk', charset='utf8')
    cursor = conn.cursor()

    # 기존 해시값 가져오기(해시값 비교 추가 수정 중)
    cursor.execute("SELECT filename, md5 FROM md5")
    db_file_hash = cursor.fetchall()
    for data in db_file_hash:
        print(db_file_ha[1])
    file_hash = list(db_file_hash )
    print(file_hash)
    file_name = []


    options = Options()

    # 옵션 설정
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    options.add_argument('user-agent=' + user_agent)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option('prefs', {
        "download.default_directory": "C:\\Users\\quddu\\Desktop\\apk",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True})
    driver = webdriver.Chrome(options=options)

    # 초기 검색어 입력
    query = 'tag:apk'

    # URL 접속
    url1 = 'https://bazaar.abuse.ch/'
    driver.get(url1)
    time.sleep(1)

    # apk 검색 결과 화면
    driver.find_element(By.XPATH, '/html/body/main/div[1]/div/p[2]/a').click()
    search_tab = driver.find_element(By.CSS_SELECTOR, '#search')
    search_tab.send_keys(query)
    search_tab.send_keys(Keys.ENTER)
    time.sleep(3)

    # apk 파일들 sha256 값 모으기


 
    # for i in range(1,4):
    for k in range(2,6):
        driver.find_element(By.XPATH, '//*[@id="samples_paginate"]/ul/li[{}]/a'.format(k)).click()
        for i in range(1,251):
            tag_td = driver.find_element(By.CSS_SELECTOR, '#samples > tbody > tr:nth-child({}) > td:nth-child(2) > a'.format(i))
            tag_href = tag_td.get_attribute('href')
            file_name.append(tag_href)

    for h in range(len(file_name)):
        url_list = file_name[h]
        driver.get(url_list)
        # 중복 검사
        file_md5 = driver.find_element(By.ID, 'md5_hash')
        if file_md5.text in file_hash:
            print(file_name[h] + "가 이미 존재합니다.")
            continue

        file_hash.append(file_md5.text)
        sql = "INSERT INTO md5(filename, md5) values(%s, %s)"
        val = (file_name[h], file_hash[h])
        cursor.execute(sql, val)
        # 중복 아닐 경우 다운 진행 
        driver.find_element(By.XPATH, '/html/body/main/table/tbody/tr[7]/td/a').click()
        
        tag_div = driver.find_element(By.CSS_SELECTOR, 'body > main > div.container.text-center')
        tag_button = tag_div.find_element(By.TAG_NAME, 'button')
        tag_id = tag_button.get_attribute('id')
        driver.find_element(By.XPATH, '//*[@id="{}"]'.format(tag_id)).click()
        time.sleep(2)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    #데이터베이스 연결
    crawling()
