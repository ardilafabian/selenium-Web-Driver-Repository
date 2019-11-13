from sys import stdin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pandas import DataFrame
import requests, shutil, os

browser = webdriver.Chrome("./chromeDriverExec/ver77-0-3865-10/chromedriver")

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

def exportProductsData(items, name_file):
    df = DataFrame(items, columns= ['name', 'sku', 'size', 'description', 'img_url'])
    export_excel = df.to_excel(r'./exported_files/' + name_file + '.xlsx', index=None, header=True)
    print("\nArchivo " + name_file + ".xlsx generado.\n")

def exportImagesData(imagesData, name_file):
    df = DataFrame(imagesData, columns=['code', 'image_url'])
    export_excel = df.to_excel(r'./exported_files/' + name_file + '.xlsx', index=None, header=True)
    print("\nArchivo " + name_file + ".xlsx generado.\n")

def getImageURL(code):
    res = ""

    searchBar = browser.find_element_by_name("q")
    searchBar.send_keys(code)
    searchBar.submit()

    try:
        #Main image showed in the initial search of google images
        element = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='rg_s']/div[1]/a[1]"))
        )

        href = element.get_attribute("href")

        print("\nURL ->")
        print(href)

        #Verify if URL is valid and refresh page in case the URL is not valid
        if href[-13:] == "gws-wiz-img.#":
            print("Try search one more time...")
            browser.refresh()

            element = WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='rg_s']/div[1]/a[1]"))
            )

            href = element.get_attribute("href")

        print("\nURL ->")
        print(href)

        #Only check if the URL is valid
        if isinstance(href, str) and href[-13:] != "gws-wiz-img.#":

            browser.get(href)

            image = WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='irc_cc']/div/div[2]/div[1]/div[2]/div[1]/a/div/img"))
            )

            res = image.get_attribute("src")
        else:
            res = "null"
        print(res)
    except (StaleElementReferenceException, TimeoutException) as e:
        print("It failed.")
        res = "null"

    return res

def getCodeImages(codes):
    imagesData = {
        "code" : [],
        "image_url" : [],
    }

    for c in codes:
        print("\n//------------------------//")
        print("code -> " + c)
        imagesData['code'].append(c)

        #Go to find the URL of the image
        image_url = getImageURL(c)
        imagesData['image_url'].append(image_url)

        #Obtain again Google images page result
        browser.get("https://www.google.com/imghp?hl=es")

    return imagesData

def printMenu():
    print("\nMenú:")
    print("\r1. Descargar info de productos de link de la página 'Euro Supermercados'")
    print("\r2. Descargar URLs de imagenes de una lista de códigos")
    print("\r0. Salir")

def startProcessChoiceOne(name_file):
    #Ask URL to the User
    url = input("\nIngresa la URL:\n").strip()

    #Ask number of pages to the User
    n = int(input("Ingresa numero de paginas:\n").strip())

    #Number of pages
    items_url = getItemsUrl(n, url)

    #Get all the products information
    itemsDictionary = getItemsInformation(items_url)

    #Export Information (specify name)
    exportProductsData(itemsDictionary, name_file)

def make_dir(dirname):
    current_path = os.getcwd()
    path = os.path.join(current_path, dirname)
    if not os.path.exists(path):
        os.makedirs(path)

def save_image_to_file(image, dirname, img_name):
    with open(r'./{dirname}/{img_name}.png'.format(dirname=dirname, img_name=img_name), 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)

def download_images(dirname, img_dictionary):
    links = img_dictionary['image_url']
    codes = img_dictionary['code']
    length = len(links)
    for index, link in enumerate(links):
        print('Downloading {0} of {1} images'.format(index + 1, length))
        if link != "null":
            response = requests.get(link, stream=True)
            img_name = codes[index].replace(" ", ",")
            save_image_to_file(response, dirname, img_name)
            del response

def startProcessChoiceTwo(name_file):
    #Ask for codes
    print("Ingresa la lista de códigos:\n")
    codes = []
    input_code = stdin.readline().strip()
    while input_code != "":
        codes.append(input_code)
        input_code = stdin.readline().strip()

    print("\nPor favor espera, esto puede tardar unos minutos...\n\n")

    #Obtain Google images page result
    browser.get("https://www.google.com.co/imghp?hl=es-419&tab=wi&ogbl")

    #Get all images information
    imagesDictionary = getCodeImages(codes)

    #Export Information (specify name)
    exportImagesData(imagesDictionary, name_file)

    #Create directory for images
    dirname = 'exported_files/' + name_file
    make_dir(dirname)

    #Download images
    download_images(dirname, imagesDictionary)

def main():
    #Show menu
    choice = -1
    while choice != 0:
        printMenu()

        #Ask choice
        choice = int(input("\nElige la opción: ").strip())

        if choice != 0:
            #Ask name of the file to be exported
            name_file = input("\nIngresa el nombre del archivo a exportar:\n").strip().replace(" ", "_")

        if choice == 1:
            startProcessChoiceOne(name_file)
        elif choice == 2:
            startProcessChoiceTwo(name_file)

    browser.quit()

main()
