from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome("C:\\Users\\Fabian Ardila\\Desktop\\chromedriver.exe")

def getItemsUrl(numPages):
    j=1
    url = "https://www.eurosupermercados.com/categoria-de-producto/abarrotes/page/"
    items_urls = []
    while j <= numPages:
        browser.get(url + str(j) + "/")
        items = browser.find_elements_by_xpath("//li[contains(@class,'product-type-simple')]/a")
        for i in items:
            items_urls.append(i.get_attribute('href'))
        j += 1
    return items_urls

def main():
    items_url = getItemsUrl(2)

    for i in range(len(items_url)):
        print("item #" + str(i+1) + " " + items_url[i])
main()
