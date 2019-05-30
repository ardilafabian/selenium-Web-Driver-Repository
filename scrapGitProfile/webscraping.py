from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

browser = webdriver.Chrome(executable_path="C:\\Users\\Fabian Ardila\\Desktop\\chromedriver.exe", chrome_options=option)
browser.get("https://github.com/TheDancerCodes")
