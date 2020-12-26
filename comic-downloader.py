from selenium import webdriver
import urllib.request
import os  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def wait_until_find_elements_by_xpath(driver, xpath, url):
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            return elements
        except Exception as e:
            print('wait_until_find_elements_by_xpath: ', e)
            driver.get(url)

def wait_until_find_element_by_xpath(driver, xpath, url):
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return element
        except Exception as e:
            print('wait_until_find_element_by_xpath: ', e)
            driver.get(url)


def goto_next_page_or_chapter():
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[.='下一頁']"))).click()
        return True
    except Exception as e:
        print('goto_next_page_or_chapter: ', e)
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[.='下一話']")))
        if(element):
            element.click()
            #break
            return False
        else:
            driver.close()
            f.close()
            exit(0)

# 基本設定、路徑等等都在這裡
root_path = 'H:\野良神'
chapter_start_from = 1
# 山立漫畫 - 你要下載的漫畫的首頁
index_url = 'https://www.setnmh.com/comic-lpdaj-%E9%87%8E%E8%89%AF%E7%A5%9E'

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
driver.find_element_by_xpath("//span[.='全部目錄']").click()

print("Current Page Title is : %s" %driver.title)

# 整理成字典，用字典來找 url
for element in wait_until_find_elements_by_xpath(driver, '//ul[@id="ul_chapter1"]/li/a', index_url):
    url_chapter = element.get_attribute('href')
    folderName = element.get_attribute('title').rstrip()
    print(folderName)
    print(url_chapter)
    chapters.setdefault(folderName, url_chapter)

if not os.path.exists(root_path):
    os.makedirs(root_path)

# 曾經下載過的 url 會被記錄到檔案上，避免重複下載
filepath_download_hisoty = root_path + '\download_history.txt'
open(filepath_download_hisoty, 'a+')
f = open(filepath_download_hisoty, 'r')
download_history = set(line.strip() for line in f)
f.close()

# 從第一話開始下載
chapter_index = 1
for keys_chapter in reversed(chapters.keys()):
    # 如果想要跳過前面的章節，可以設定 chapter_start_from 變數
    if(chapter_index < chapter_start_from):
        print("skip chapter: ", chapter_index)
        chapter_index += 1
        continue

    # 頁面跳轉到該 chapter 的頁面
    driver.get(chapters[keys_chapter])

    # 建立該章節的資料夾
    download_dir = root_path + '\\' + keys_chapter
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # 從該章節的第一頁開始下載
    filename = 1
    count = 1
    while True:
        # 取得該頁面的 image url
        image_element = wait_until_find_element_by_xpath(driver, "//div[@class='ptview']/img", chapters[keys_chapter])
        url_img = image_element.get_attribute('src')

        # 如果已經下載過該圖片了，則跳過下載到下一頁
        # 如果已經是最後一頁了，則跳轉到下一個 chapter
        # 全部下載完則程式結束
        if(url_img in download_history):
            filename = str(count) + '.jpg'
            print(download_dir + '\\' + filename + " already exist")
            count += 1

            if goto_next_page_or_chapter():
                continue
            else:
                break
        else:
            # 開始下載
            req = urllib.request.Request(url_img, headers=headers)
            data = urllib.request.urlopen(req).read()
            filename = str(count) + '.jpg'
            with open(download_dir + '\\' + filename, 'wb') as f:
                f.write(data)
                f.close()
            count = count + 1

            # 印出目前下載的資訊
            print(url_img)
            print(download_dir + '\\' + filename)

            # 下載完成後，紀錄到 download_history set 中，以及 filepath_download_hisoty 的檔案
            download_history.add(url_img)
            f = open(filepath_download_hisoty, 'a')
            f.write(str(url_img) + '\n')
            f.close()

        if goto_next_page_or_chapter():
            continue
        else:
            break