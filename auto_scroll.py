import time
from selenium import webdriver

chromeDriver = 'D:\github\chromedriver.exe' 

from selenium import webdriver  
import time  
#訪問百度  
driver = webdriver.Chrome(executable_path=chromeDriver) 
driver.get("https://hsng.csie.io/courses/2020/IoT/")  
time.sleep(5)
for i in range(10000):
    time.sleep(0.005)
    js="var q=document.documentElement.scrollTop=" + str(i)
    driver.execute_script(js)  

# time.sleep(3)  
# #將頁面滾動條拖到底部  
# js="var q=document.documentElement.scrollTop=10000"  
# driver.execute_script(js)  
# time.sleep(3)  
# #將滾動條移動到頁面的頂部  
# js="var q=document.documentElement.scrollTop=0"  
# driver.execute_script(js)  
# time.sleep(3)  
# #將頁面滾動條移動到頁面任意位置，改變等於號後的數值即可  
# js="var q=document.documentElement.scrollTop=50"  
# driver.execute_script(js)  