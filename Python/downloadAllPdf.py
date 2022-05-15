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
from selenium.webdriver.chrome.options import Options
import requests
import os

main_url = 'http://illinois-cs418.github.io/schedule' #url 
download_folder = ""
file_ext = ['pdf']

# uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,driver):
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    # soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    r=requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser') #beautiful soup object to be used for parsing html content
    return soup

# extracts all urls from the Main Page
def scrape_main_page(main_url,driver):
    print ('-'*20,'Scraping the Main page','-'*20)
    file_links = []

    #execute js on webpage to load faculty listings on webpage and get ready to parse the loaded HTML 
    soup = get_js_soup(main_url,driver)     
    for link_holder in soup.find_all('a'): # get list of all <div> of class 'name'
        rel_link = link_holder.get('href', [])  # get url
        # check if the url ends with the target file extesion given in the list file_ext
        if len(rel_link) >4 and rel_link[-4] == '.' and rel_link[-3:] in file_ext:
            file_links.append(rel_link) 
    print ('-'*20,'Found {} file urls'.format(len(file_links)),'-'*20)
    return file_links

# create a webdriver object and set options for headless browsing
options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver',options=options)

# get all the file links
file_links = scrape_main_page(main_url,driver)

# Scrape homepages of all urls
tot_urls = len(file_links)
for i,link in enumerate(file_links):
    print ('-'*20,'Scraping url {}/{}'.format(i+1,tot_urls),'-'*20)
    # Write content in pdf file
    file_name = link.split("/")[-1]
    download_path = os.path.join(download_folder,file_name)
    response = requests.get(link)
    pdf = open(file_name, 'wb')
    pdf.write(response.content)
    pdf.close()
    print("File ", i+1, " downloaded")
driver.close()