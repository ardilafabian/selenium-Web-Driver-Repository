from selenium import webdriver
from selenium.webdriver.common.by import By
from pandas import DataFrame

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

def getItemInfo(url):
    browser.get(url)
    info = {
        "name":"",
        "sku":"",
        "size":"",
        "description":"",
        "img_url":"",
    }

    #Validate Name if have size in it
    name = browser.find_elements_by_xpath("//div[@class='content-area']/div/div[2]/div[2]/h1")[0].text
    res = name.find("*")
    if res != -1:
        info['name'] = name[:res]
        info['size'] = name[res+1:]
    else:
        info['name'] = name
        info['size'] = "null"

    #Find sku
    sku = browser.find_elements_by_xpath("//div[@class='sku_wrapper']/span")[0].text
    info['sku'] = sku

    #Find description
    description = browser.find_elements_by_xpath("//div[@id='tab-description']/p")[0].text
    info['description'] = description

    #find image img_url
    img_url = browser.find_elements_by_xpath("//div[@class='content-area']/div/div[2]/div[1]/div/a/img")[0]
    info['img_url'] = img_url.get_attribute('src')

    return info

def main():
    #items_url = getItemsUrl(2)

    itemInfo = getItemInfo("https://www.eurosupermercados.com/tienda/zumo-uva-2lt-light-menal/")
    print(itemInfo)

    #for i in range(len(items_url)):
        #print("item #" + str(i+1) + " " + items_url[i])

    browser.quit()
main()
