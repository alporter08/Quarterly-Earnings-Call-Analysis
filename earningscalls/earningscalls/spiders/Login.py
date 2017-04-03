# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response
from scrapy.http import Response,FormRequest,Request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import os


class LoginSpider(scrapy.Spider):
    name = "Login"
    allowed_domains = ["seekingalpha.com"]
    start_urls = ['https://seekingalpha.com/account/login/']


    def get_cookies(self):
        base_url = 'https://seekingalpha.com/account/login/'
        chromedriver = "/Applications/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        driver.implicitly_wait(30)
        driver.get(base_url)

        driver.implicitly_wait(5) # seconds


        username_form = driver.find_element_by_id("login_user_email")
        username_form.send_keys("crostucicr@housat.com")
        password = driver.find_element_by_id("login_user_password")
        password.send_keys("crostucicr@housat.com")


        button=driver.find_element_by_xpath('//*[@id="orthodox_login"]/div[5]/input')
        button.click()

        cookies = driver.get_cookies()
        driver.close()
        return cookies


    # def login(self, response):
    #     return scrapy.FormRequest.from_response(
    #         response,
    #         formid='orthodox_login',
    #         formdata={'login_user_email': 'cislakasti@housat.com', 'login_user_password': 'passw0rd'},
    #         clickdata={'value': 'Sign in'},
    #         callback=self.after_login
    #         )

    def parse(self, response):
        return Request(url="https://seekingalpha.com/account/login",
            cookies=self.get_cookies(),
            callback=self.after_login)

    def after_login(self, response):
        # check login succeed before going on
        if "Please verify you are not a bot" in response.body:
            inspect_response(response, self)
            self.logger.error("Login failed")
            return
        else:
            urls = ['http://seekingalpha.com/symbol/C/earnings/more_transcripts?page=1',
            'http://seekingalpha.com/symbol/C/earnings/more_transcripts?page=2',
            'http://seekingalpha.com/symbol/C/earnings/more_transcripts?page=3']

            for url in urls:
                yield scrapy.Request(url,
                callback=self.get_transcripts)

    def get_transcripts(self, response):
        url_ends = []
        for link in response.xpath('.//a[contains(@href, "results")]/@href').extract():
            link = link.split('"')[1]
            link = link.replace("\\", "")
            url_ends.append(link)
        for url_end in url_ends:
            url = 'http://seekingalpha.com' + url_end + '?part=single'
            yield scrapy.Request(url,
            callback=self.parse_transcript)

    def parse_transcript(self, response):
        key = response.xpath('.//h1/text()').extract()
        t_dict = {}
        t_list = []
        for i in response.xpath('//*[@id="a-body"]/p'):
            t_list.append(i.extract())
        t_dict[key[0]] = t_list
        yield t_dict




        # continue scraping with authenticated session...
