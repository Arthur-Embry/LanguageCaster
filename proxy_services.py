from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from typing import Union
from pydantic import BaseModel
import openai
import requests
from bs4 import BeautifulSoup
import re
#security key for openai
openai.api_key = "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"
#driver path
driver_path = b'C:\Users\user\Desktop\chromedriver\chromedriver.exe'
class proxy_links_params(BaseModel):
    query: Union[str,None]=""
    domain: Union[str,None]=""
    acceptlanguage: Union[str,None]="en-US,en;q=0.9"
    dnt: Union[str,None] = "1"
    secchua: Union[str,None] = '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"'
    secchuamobile: Union[str,None] = '?0'
    secchuaplatform: Union[str,None] = '"Windows"'
    secfetchdest: Union[str,None] = 'empty'
    useragent: Union[str,None] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'

def proxy_links_run(item: proxy_links_params):

    #set headers
    req_headers = {
    'accept-language':item.acceptlanguage,
    'dnt':item.dnt,
    'sec-ch-ua':item.secchua,
    'sec-ch-ua-mobile':item.secchuamobile,
    'sec-ch-ua-platform':item.secchuaplatform,
    'sec-fetch-dest':item.secfetchdest,
    'user-agent':item.useragent
    }

    #throw to maintain subject specific
    google_domains = ('https://www.google.', 
                    'https://google.', 
                    'https://webcache.googleusercontent.', 
                    'http://webcache.googleusercontent.', 
                    'https://policies.google.',
                    'https://support.google.',
                    'https://maps.google.',
                    'https://accounts.google.com')

    #get and parse
    requests_results = requests.get(item.url, headers=req_headers)
    soup_link = BeautifulSoup(requests_results.content, "html.parser")
    soup_title = BeautifulSoup(requests_results.text,"html.parser")
    links = soup_link.find_all("a")
    heading_object=soup_title.find_all( 'h3' )

    link_return=[]

    for link in links:
        for info in heading_object:
            link_hr = link.get('href')
            #print(link_hr)
            link_href=str(link_hr)
            if not link_href in link_return and "https://" in link_href and not link_href.startswith(google_domains):
                link_return.append(link_href)

    #return response
    return link_return

class proxy_paragraphs_params(BaseModel):
    url: Union[str,None]=""
    acceptlanguage: Union[str,None]="en-US,en;q=0.9"
    dnt: Union[str,None] = "1"
    secchua: Union[str,None] = '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"'
    secchuamobile: Union[str,None] = '?0'
    secchuaplatform: Union[str,None] = '"Windows"'
    secfetchdest: Union[str,None] = 'empty'
    useragent: Union[str,None] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'

def proxy_paragraphs_run(item: proxy_paragraphs_params):

    #set headers
    req_headers = {
    'accept-language':item.acceptlanguage,
    'dnt':item.dnt,
    'sec-ch-ua':item.secchua,
    'sec-ch-ua-mobile':item.secchuamobile,
    'sec-ch-ua-platform':item.secchuaplatform,
    'sec-fetch-dest':item.secfetchdest,
    'user-agent':item.useragent
    }

    #make request, and parse html
    req = requests.get(item.url, headers=req_headers)
    soup = BeautifulSoup(req.text, 'html.parser')

    #remove scripts and styles from soup
    for script in soup(["script", "style"]):
        script.extract()

    inner_p=""
    #combine innertext from all noncap tags of type p
    for tag in soup.find_all('p'):
        if tag.text.isupper()==False:
            inner_p+=tag.text+"\n"

    #remove extra lines, non-ascii characters, and extra spaces
    inner_p=re.sub(r'\n\s*\n', '\n\n', inner_p)
    inner_p = re.sub(r'[^\x00-\x7F]+',' ', inner_p)
    inner_p = re.sub(r'\s{2,}',' ', inner_p)

    #return response
    return inner_p

class proxy_chromium_params(BaseModel):
    url: Union[str,None]=""
    acceptlanguage: Union[str,None]="en-US,en;q=0.9"
    dnt: Union[str,None] = "1"
    secchua: Union[str,None] = '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"'
    secchuamobile: Union[str,None] = '?0'
    secchuaplatform: Union[str,None] = '"Windows"'
    secfetchdest: Union[str,None] = 'empty'
    useragent: Union[str,None] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'

def proxy_chromium_run(item: proxy_chromium_params):
    chrome_options = Options()
    driver = webdriver.Chrome(driver_path,options=chrome_options)

    # Create a request interceptor
    def interceptor(request):
        #spoof the headers
        del request.headers['accept-language']
        request.headers['accept-language'] = item.acceptlanguage
        del request.headers['dnt']
        request.headers['dnt'] = item.dnt
        del request.headers['sec-ch-ua']
        request.headers['sec-ch-ua'] = item.secchua
        del request.headers['sec-ch-ua-mobile']
        request.headers['sec-ch-ua-mobile'] = item.secchuamobile
        del request.headers['sec-ch-ua-platform']
        request.headers['sec-ch-ua-platform'] = item.secchuaplatform
        del request.headers['sec-fetch-dest']
        request.headers['sec-fetch-dest'] = item.secfetchdest
        del request.headers['user-agent']
        request.headers['user-agent'] = item.useragent
        
    # Set the interceptor on the driver
    driver.request_interceptor = interceptor

    driver.get(item.url)
    #execute script to scroll down the page on bind scraping to pageload
    driver.execute_script("""window.onload = function() {
        window.scrollTo(0, document.body.scrollHeight);
        var el = document.createElement('div');
        el.id = 'scriptload';
        el.innerHTML = 'Hello World';
        document.body.appendChild(el);
    };""")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "scriptload"))
        )
    finally:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup.html.prettify

class html_reduction_params(BaseModel):
    text: Union[str,None]=""
    reduction_type: Union[str,None]="paragraphs"

def html_reduction_run(item: html_reduction_params):
    if item.reduction_type=="paragraphs":
        soup = BeautifulSoup(item.text, 'html.parser')

        #remove scripts and styles from soup
        for script in soup(["script", "style"]):
            script.extract()

        inner_p=""
        #combine innertext from all noncap tags of type p
        for tag in soup.find_all('p'):
            if tag.text.isupper()==False:
                inner_p+=tag.text+"\n"

        #remove extra lines, non-ascii characters, and extra spaces
        inner_p=re.sub(r'\n\s*\n', '\n\n', inner_p)
        inner_p = re.sub(r'[^\x00-\x7F]+',' ', inner_p)
        inner_p = re.sub(r'\s{2,}',' ', inner_p)

        #return response
        return inner_p
    elif item.reduction_type=="html":
        soup = BeautifulSoup(item.text, 'html.parser')

        #remove scripts and styles from soup
        for script in soup(["script", "style"]):
            script.extract()

        #return response
        return soup.html.prettify
    elif item.reduction_type=="text":
        soup = BeautifulSoup(item.text, 'html.parser')

        #remove scripts and styles from soup
        for script in soup(["script", "style"]):
            script.extract()

        inner_text=soup.get_text

        #remove extra lines, non-ascii characters, and extra spaces
        inner_text=re.sub(r'\n\s*\n', '\n\n', inner_text)
        inner_text = re.sub(r'[^\x00-\x7F]+',' ', inner_text)
        inner_text = re.sub(r'\s{2,}',' ', inner_text)

        #return response
        return soup.get_text()

    elif item.reduction_type=="links":

        #remove scripts and styles from soup
        for script in soup(["script", "style"]):
            script.extract()

            soup_link = BeautifulSoup(item.text, "html.parser")
            soup_title = BeautifulSoup(item.text,"html.parser")
            links = soup_link.find_all("a")
            heading_object=soup_title.find_all( 'h3' )

            link_return=[]

            for link in links:
                for info in heading_object:
                    link_hr = link.get('href')
                    #print(link_hr)
                    link_href=str(link_hr)
                    if not link_href in link_return and "https://" in link_href:
                        link_return.append(link_href)

        #return response
        return link_return