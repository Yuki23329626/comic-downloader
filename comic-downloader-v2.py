import time
from selenium import webdriver
import urllib.request
import os  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
import logging
import re
from fake_useragent import UserAgent
ua = UserAgent()

FORMAT = '[%(levelname)s][%(asctime)s] %(message)s'
logging.basicConfig(handlers=[logging.FileHandler(filename='log.comic-downloader', encoding='utf-8')], format=FORMAT, level=logging.WARNING)

def wait_until_find_elements_by_xpath(driver, xpath, url):
    ttl = 5
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            elements = driver.find_elements_by_xpath(xpath)
            return elements
        except Exception as e:
            print('Retry:', ttl)
            time.sleep(1)
            ttl -= 1
            # print('Error: wait_until_find_elements_by_xpath()')
            if ttl < 1:
                logging.error(e)
                driver.get(url)
                try:
                    driver.find_element_by_xpath("//span[.='點擊此處繼續閱讀']").click()
                except Exception as e:
                    pass
                driver.find_element_by_xpath("//span[.='全部目錄']").click()
                ttl = 5

def wait_until_find_element_by_xpath(driver, xpath, url):
    ttl = 5
    while True:
        try:
            # wait = WebDriverWait(driver, 10)
            # element = wait.until(EC.presence_of_all_element_located((By.XPATH, xpath)))
            element = driver.find_element_by_xpath(xpath)
            return element
        except Exception as e:
            print('Retry:', ttl)
            time.sleep(1)
            ttl -= 1
            # print('Error: wait_until_find_element_by_xpath()')
            if ttl < 1:
                logging.error(e)
                logging.error(url)
                driver.get(url)
                ttl = 5


def goto_next_page_or_chapter(driver, filename, fptr):
    ttl = 5
    while ttl > 0:
        try:
            driver.find_element_by_xpath("//a[.='下一頁']").click()
            return True
        except Exception as e:
            print('Retry next_page:', ttl)
            time.sleep(1)
            ttl -= 1
    print('\n===== Go to next chapter =====')
    ttl = 5
    while ttl > 0:
        try:
            driver.find_element_by_xpath("//a[.='下一話']").click()
            return False
        except Exception as e:
            print('Retry:', ttl)
            time.sleep(1)
            ttl -= 1
            if ttl < 1:
                print('\n===== Can not find the next chapter =====')
                print('\n===== Process existing =====')
                print('\nCurrent filename: ' + filename)
                logging.error('Can not find the next chapter, process existing...')
                logging.error('Current filename: ' + filename)
                driver.close()
                fptr.close()
                exit(0)

# 基本設定、路徑等等都在這裡
# root_path = 'H:\野良神\\'
root_path = 'H:\無良公會\\'
chapter_start_from = 29
page_start_from = 4
# 山立漫畫 - 你要下載的漫畫的首頁
# index_url = 'https://www.setnmh.com/comic-lpdaj-%E9%87%8E%E8%89%AF%E7%A5%9E'
index_url = 'https://www.setnmh.com/comic-lvcnh-%E7%84%A1%E8%89%AF%E5%85%AC%E6%9C%83'

# 啟動chrome瀏覽器
# chromedriver檔案放的位置，請自行下載 chromeDriver， google 搜尋 "chromeDriver" 即可，請下載當前電腦安裝的 chrome 版本的 Driver
chromeDriver = 'D:\github\chromedriver.exe' 
# 背景執行
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=chromeDriver) 
# 前景執行
#driver = webdriver.Chrome(executable_path=chromeDriver) 

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
# headers = {'User-Agent':str(ua.chrome)}

# 目錄的 dictionary
chapters = {}
driver.get(index_url)
try:
    driver.find_element_by_xpath("//span[.='點擊此處繼續閱讀']").click()
except Exception as e:
    pass
wait_until_find_element_by_xpath(driver, "//span[.='全部目錄']", index_url).click()

print("Current Page Title is : %s" %driver.title)

# 整理成字典，用字典來找 url
for element in wait_until_find_elements_by_xpath(driver, '//ul[@id="ul_chapter1"]/li/a', index_url):
    print("Current Page Title is : %s" %driver.title)
    url_chapter = element.get_attribute('href')
    folderName = element.get_attribute('title').rstrip()
    print(folderName)
    print(url_chapter)
    chapters.setdefault(folderName, url_chapter)

if not os.path.exists(root_path):
    os.makedirs(root_path)

# 曾經下載過的 url 會被記錄到檔案上，避免重複下載
filepath_download_hisoty = root_path + 'download_history.txt'
open(filepath_download_hisoty, 'a+')
f = open(filepath_download_hisoty, 'r')
download_history = set(line.strip() for line in f)
f.close()

chapter_index = 1
# list_keys_chapter = []
# for key in chapters.keys():
#     list_keys_chapter.append(key)

# 從第一話開始下載
for keys_chapter in reversed(chapters.keys()): # 僅 python 3.8 以後適用 reversed(dictionary.keys())
#for keys_chapter in reversed(list_keys_chapter): 
    # 如果想要跳過前面的章節，可以設定 chapter_start_from 變數
    if(chapter_index < chapter_start_from):
        print("skip chapter: ", chapter_index)
        chapter_index += 1
        continue

    # 頁面跳轉到該 chapter 的頁面，並且從 page_start_from 的頁數開始下載
    if(page_start_from > 1):
        chapter_url = chapters[keys_chapter]
        url_head = [m.start() for m in re.finditer('-', chapters[keys_chapter])][-2] + 1
        url_tail = [m.start() for m in re.finditer('-', chapters[keys_chapter])][-1]
        driver.get(chapter_url[:url_head] + str(page_start_from) + chapter_url[url_tail:])
    else:
        driver.get(chapters[keys_chapter])
    
    # 開始下載
    print("\nDownload image start from page", page_start_from)
    page_index = page_start_from
    while True:
        # 取得該頁面的 image url
        image_element = wait_until_find_element_by_xpath(driver, "//div[@class='ptview']/img", driver.current_url)
        url_img = image_element.get_attribute('src')

        # 如果已經下載過該圖片了，則跳過下載到下一頁
        # 如果已經是最後一頁了，則跳轉到下一個 chapter
        # 全部下載完則程式結束
        if(url_img in download_history):
            filename = str(page_index) + '.jpg'
            print(root_path + str(chapter_index) + '-' + filename + " already exist")
            page_index += 1

            if goto_next_page_or_chapter(driver, root_path + str(chapter_index) + '-' + filename, f):
                continue
            else:
                chapter_index += 1
                page_start_from = 1
                break
        else:
            # 開始下載
            req = urllib.request.Request(url_img, headers=headers)
            data = urllib.request.urlopen(req).read()
            filename = str(page_index) + '.jpg'
            with open(root_path + str(chapter_index) + '-' + filename, 'wb') as f:
                f.write(data)
                f.close()
            page_index = page_index + 1

            # 印出目前下載的資訊
            print(url_img)
            print(root_path + str(chapter_index) + '-' + filename)

            # 下載完成後，紀錄到 download_history set 中，以及 filepath_download_hisoty 的檔案
            download_history.add(url_img)
            f = open(filepath_download_hisoty, 'a')
            f.write(str(url_img) + '\n')
            f.close()

        if goto_next_page_or_chapter(driver, root_path + str(chapter_index) + '-' + filename, f):
            continue
        else:
            chapter_index += 1
            page_start_from = 1
            break