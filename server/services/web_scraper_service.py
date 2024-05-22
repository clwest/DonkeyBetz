import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import subprocess
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_with_scrapy(url, title, collection):
    try:
        spider_name = "web_scraper_spider"
        settings = {
            'FEEDS': {
                'output.json': {
                    'format': 'json',
                    'overwrite': True
                }
            }
        }

        process = subprocess.Popen(
            ['scrapy', 'crawl', spider_name, '-a', f'url={url}', '-a', f'title={title}', '-a', f'collection={collection}'],
            cwd=os.path.join(os.getcwd(), 'server/web_scraper'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()

        if process.returncode == 0:
            with open(os.path.join(os.getcwd(), 'server/web_scraper/output.json')) as f:
                data = json.load(f)
                return data
        else:
            raise Exception(stderr.decode())

    except Exception as e:
        return None


def scrape_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    html_content = driver.page_source
    driver.quit()
    return html_content