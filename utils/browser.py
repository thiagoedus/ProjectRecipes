import os

from selenium import webdriver
from pathlib import Path
from time import sleep
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME

#  --headless - O headless não mostra o navegador abrindo
def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('http://www.udemy.com.br')
    sleep(5)
    browser.quit()