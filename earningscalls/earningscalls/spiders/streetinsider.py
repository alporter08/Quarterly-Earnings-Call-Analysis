# -*- coding: utf-8 -*-
import scrapy


class StreetinsiderSpider(scrapy.Spider):
    name = "streetinsider"
    allowed_domains = ["streetinsider.com"]
    start_urls = ['http://streetinsider.com/']

def get_cookies(self):
    base_url = 'https://www.streetinsider.com/'
    chromedriver = "/Applications/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver


    driver = webdriver.Chrome(chromedriver)
    driver.get("https://www.streetinsider.com/ec_earnings.php?q=gs")

    driver.implicitly_wait(5) # seconds

    cookies = driver.get_cookies()
    driver.close()
    return cookies



# def parse(self, response):
#     return Request(url="https://www.streetinsider.com/ec_earnings.php?q=gs",
#         cookies=self.get_cookies(),
#         callback=self.parse_gs)
#
# def parse_gs(self, response):
#     surprise = driver.find_element_by_xpath('//*[@id="content"]/table[1]/tbody/tr[4]/td[6]/span').extract()
