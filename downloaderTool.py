from sys import stdin
from selenium import webdriver
from selenium.webdriver.common.by import By
from pandas import DataFrame

browser = webdriver.Chrome(".\\executables\\chromedriver_win32\\chromedriver.exe")

def getItemsUrl(numPages, url_provided):
    j=1

    if url_provided[-1] == "/":
        url = url_provided + "page/"
    else:
        url = url_provided + "/page/"

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

    """Validate Name if have size in it"""
    name = browser.find_elements_by_xpath("//div[@class='content-area']/div/div[2]/div[2]/h1")[0].text
    res = name.find("*")
    if res != -1:
        info['name'] = name[:res]
        info['size'] = name[res+1:]
    else:
        info['name'] = name
        info['size'] = "null"

    """Find sku"""
    sku = browser.find_elements_by_xpath("//div[@class='sku_wrapper']/span")
    if len(sku) > 0:
        info['sku'] = sku[0].text
    else:
        info['sku'] = 'null'

    """Find description"""
    description = browser.find_elements_by_xpath("//div[@id='tab-description']/p")
    if len(description) > 0:
        info['description'] = description[0].text
    else:
        info['description'] = 'null'

    """find image url"""
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

def exportProductsData(items, name_file):
    df = DataFrame(items, columns= ['name', 'sku', 'size', 'description', 'img_url'])

    export_excel = df.to_excel(r'.\\exported_files\\' + name_file + '.xlsx', index=None, header=True)

    print(df)

def printMenu():
    print("\nMenu:")
    print("\r1. Descargar info de productos de link de la pagina 'Euro Supermercados'")
    print("\r2. Descargar URLs de imagenes de una lista de codigos")
    print("\r0. Salir")

def startProcessChoiseOne():
    """Ask URL to the User"""
    url = input("\nIngresa la URL:\n").strip()

    """Ask number of pages to the User"""
    n = int(input("Ingresa numero de paginas:\n").strip())

    """Ask name of the file to be exported"""
    name_file = input("Ingresa el nombre del archivo a exportar:\n").strip()

    """Number of pages"""
    items_url = getItemsUrl(n, url)

    """Get all the products information"""
    itemsDictionary = getItemsInformation(items_url)

    """Export Information (specify name)"""
    exportProductsData(itemsDictionary, name_file)

def startProcessChoiseTwo():
    print("Ingresa la lista de códigos:\n")
    code = stdin.readline().strip()
    while code != "":
        
        phoneNumber = stdin.readline().strip()

def main():
    """Show menu"""
    choise = -1
    while choise != 0:
        printMenu()

        choise = int(input("\nElige la opción: ").strip())

        if choise == 1:
            startProcessChoiseOne()
        else if choise == 2:
            startProcessChoiseTwo()

    browser.quit()

    print("¡Terminado!")
main()
