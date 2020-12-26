# comic-downloader
A comic downloader in Python with Selenium.

## 需求
1. python 3.8.7  
2. urllib3 1.26.2  
3. selenium 3.141.0  
4. chromedriver.exe  
請自行下載 chromeDriver， google 搜尋 "chromeDriver" 即可，請下載當前電腦安裝的 chrome 版本的 Driver  
完成之後在 ./comic-downloader.py 設定 chromeDriver.exe 的檔案路徑  

## How to use
1. 在 comic-downloader.py 裡設定下載的網址，以及下載資料夾的路徑
```
# 基本設定、路徑等等都在這裡
root_path = 'H:\野良神'
chapter_start_from = 1
# 山立漫畫 - 你要下載的漫畫的首頁
index_url = 'https://www.setnmh.com/comic-lpdaj-%E9%87%8E%E8%89%AF%E7%A5%9E'

```
2. 執行
```bash
python comic-downloader.py
```
