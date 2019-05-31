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

def getImageURL(code):
    res = ""

    searchBar = browser.find_element_by_name("q")
    searchBar.send_keys(code)
    searchBar.submit()

    linkToImage = browser.find_elements_by_xpath("//div[@data-ri='0']/div")
    if len(linkToImage) > 0:
        linkToImage = linkToImage[0].get_attribute('class')
        print("JSON meta image -> " + linkToImage)
    else:
        res = "null"

    return res

def getCodeImages(codes):
    imagesData = {
        "code" : [],
        "image_url" : [],
    }

    for c in codes:
        imagesData['code'] = c
        imagesData['image_url'].append(getImageURL(c))

    return imagesData

def printMenu():
    print("\nMenú:")
    print("\r1. Descargar info de productos de link de la página 'Euro Supermercados'")
    print("\r2. Descargar URLs de imagenes de una lista de códigos")
    print("\r0. Salir")

def startProcessChoiceOne(name_file):
    """Ask URL to the User"""
    url = input("\nIngresa la URL:\n").strip()

    """Ask number of pages to the User"""
    n = int(input("Ingresa numero de paginas:\n").strip())

    """Number of pages"""
    items_url = getItemsUrl(n, url)

    """Get all the products information"""
    itemsDictionary = getItemsInformation(items_url)

    """Export Information (specify name)"""
    exportProductsData(itemsDictionary, name_file)

def startProcessChoiceTwo(name_file):
    """Ask for codes"""
    print("Ingresa la lista de códigos:\n")
    codes = []
    input_code = stdin.readline().strip()
    while input_code != "":
        codes.append(input_code)
        input_code = stdin.readline().strip()

    print("\nPor favor espera, esto puede tardar unos minutos...\n\n")

    """Obtain Google images page result"""
    browser.get("https://www.google.com.co/imghp?hl=es-419&tab=wi&ogbl")

    """Get all images information"""
    imagesDictionary = getCodeImages(codes)

    #"""Export Information (specify name)"""
    #exportImagesData(imagesDictionary, name_file)

def main():
    """Show menu"""
    choice = -1
    while choice != 0:
        printMenu()

        """Ask choice"""
        choice = int(input("\nElige la opción: ").strip())

        if choice != 0:
            """Ask name of the file to be exported"""
            name_file = input("\nIngresa el nombre del archivo a exportar:\n").strip()

        if choice == 1:
            startProcessChoiceOne(name_file)
        elif choice == 2:
            startProcessChoiceTwo(name_file)

    browser.quit()

    print("¡Terminado!")
main()
