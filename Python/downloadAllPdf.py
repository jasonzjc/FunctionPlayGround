# -------------------------------------------------- #
#  Jeff Zhao
#  05/14/2022
#
#  Download all PDF files from a webpage
#  Install: bs4, selenium
#
# -------------------------------------------------- #

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os

# uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,driver):
    driver.get(url)
    # res_html = driver.execute_script('return document.body.innerHTML')
    # soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    r=requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser') #beautiful soup object to be used for parsing html content
    return soup

# extracts all urls from the Main Page
def scrape_main_page(main_url,driver,file_ext):
    print ('-'*20,'Scraping the Main page','-'*20)
    file_links = []

    #execute js on webpage to load faculty listings on webpage and get ready to parse the loaded HTML 
    soup = get_js_soup(main_url,driver)     
    for link_holder in soup.find_all('a'): # get list of all <div> of class 'name'
        rel_link = link_holder.get('href', [])  # get url
        # check if the url ends with the target file extesion given in the list file_ext
        if len(rel_link) > 4 and rel_link[-4] == '.' and rel_link[-3:] in file_ext:
            file_links.append(rel_link) 
    print ('-'*20,'Found {} file urls'.format(len(file_links)),'-'*20)
    return file_links

def createwebdriver():
    # create a webdriver object and set options for headless browsing
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.google.com")
    return driver

def downloadAll(main_url,file_ext,download_folder):
    driver = createwebdriver()
    # get all the file links
    file_links = scrape_main_page(main_url,driver,file_ext)

    # Scrape homepages of all urls
    tot_urls = len(file_links)
    for i,link in enumerate(file_links):
        print ('-'*20,'Scraping url {}/{}'.format(i+1,tot_urls),'-'*20)
        # Write content in pdf file
        file_name = link.split("/")[-1]
        download_path = os.path.join(download_folder,file_name)
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        with open(download_path, 'wb') as f:
            try:
                response = requests.get(link)
                response.raise_for_status()
            except requests.exceptions.RequestException as err:
                raise SystemExit(err)
            f.write(response.content)
        print("File ", i+1, " downloaded")
    driver.close()

if __name__ == '__main__':
    
    main_url = 'http://illinois-cs418.github.io/schedule' #url 
    download_folder = "download"
    file_ext = ['pdf']
    downloadAll(main_url,file_ext,download_folder)