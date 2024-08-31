# providers:
# https://proxyscrape.com/free-proxy-list
# https://geonode.com/free-proxy-list
# https://free-proxy-list.net/

import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_proxies():
    urls = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=text&timeout=1219",
        "https://proxylist.geonode.com/api/proxy-list?protocols=http%2Chttps&limit=500&page=1&sort_by=lastChecked&sort_type=desc",
        "https://free-proxy-list.net/"
    ]
    
    src_1  = requests.get(urls[0]).text
    src_1_done = src_1.split("\r\n")
    
    src_2 = requests.get(urls[1]).json()
    src_2_done = []
    for i in src_2['data']:
        src_2_done.append(i['ip']+':'+str(i['port']))
        
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://free-proxy-list.net/')
    
    button = driver.find_element("css selector", "i.fa-clipboard")
    button.click()
    time.sleep(1)
    textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.form-control"))
    )
    src_3 = textarea.text.split("\n\n")[1]
    src_3_done = src_3.split("\n")
    driver.quit()
    
    all_proxies = src_1_done + src_2_done + src_3_done
    del src_1_done, src_2_done, src_3_done, src_1, src_2, src_3
    return all_proxies

def write_proxies(proxies):
    with open("proxies.txt", "w") as f:
        for i in proxies:
            f.write(i+'\n')

if __name__ == "__main__":
    proxies = get_proxies()
    write_proxies(proxies)
    print("Proxies written to proxies.txt")