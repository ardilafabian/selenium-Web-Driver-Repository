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
    sku = browser.find_elements_by_xpath("//div[@class='sku_wrapper']/span")
    if len(sku) > 0:
        info['sku'] = sku[0].text
    else:
        info['sku'] = 'null'

    #Find description
    description = browser.find_elements_by_xpath("//div[@id='tab-description']/p")
    if len(description) > 0:
        info['description'] = description[0].text
    else:
        info['description'] = 'null'

    #find image url
    img_url = browser.find_elements_by_xpath("//div[@class='content-area']/div/div[2]/div[1]/div/a/img")
    if len(img_url) > 0:
        info['img_url'] = img_url[0].get_attribute('src')
    else:
        info['img_url'] = 'null'

    return info

def getItemsInformation(urls):
    items = {
        "name":[],
        "sku":[],
        "size":[],
        "description":[],
        "img_url":[],
    }

    for i in urls:
        item = getItemInfo(i)
        items['name'].append(item['name'])
        items['sku'].append(item['sku'])
        items['size'].append(item['size'])
        items['description'].append(item['description'])
        items['img_url'].append(item['img_url'])

    return items

def exportData(items):


def main():
    #Number of pages
    n = 1
    items_url = getItemsUrl(n)

    #Get all the products information
    itemsDictionary = getItemsInformation(items_url)

    #Export Information
    name_file = "prodcuts_test"
    exportData(itemsDictionary)

    browser.quit()
main()
