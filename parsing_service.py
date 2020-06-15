import argparse
import os

from pip._vendor import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json


class WebScrapper:

    def __init__(self, parent_ip="127.0.0.1:8000"):
        time.sleep(5)
        self.parent_ip = parent_ip
        self.web_driver = webdriver.Remote(
            command_executor='http://firefox:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX)

    def retrieve_url(self):
        url_to_retrieve = requests.get(f"{self.parent_ip}/scrapper/latest_url")

        return url_to_retrieve

    def scrap_url(self):
        while self.retrieve_url():
            blob = self.retrieve_url()
            self.web_driver.get(f"https://www.olx.pl/oferta/{blob}.html")

            offer_titlebox = self.web_driver.find_element_by_xpath('//div[@class="offer-titlebox"]')

            title = offer_titlebox.find_element_by_tag_name("h1").text
            price = offer_titlebox.find_element_by_xpath('//strong[@class=pricelabel]').text
            quality = self.web_driver.find_element_by_xpath('//strong[@class="offer-details__value"]').text

            offer_bottombar__items = self.web_driver.find_element_by_id("offerbottombar")
            create_date = offer_bottombar__items.find_element_by_tag_name('em').find_element_by_tag_name('strong').text
            views = offer_bottombar__items.find_element_by_xpath(
                '//span[@class="offer-bottombar__counter"]/strong').text

            post_data = {"url": blob, "title": title, "price": price, "quality": quality, "created": create_date,
                         "views": views}

            requests.post(f"{self.parent_ip}/scrapper/add_data", json=json.dumps(post_data))


if __name__ == "__main__":

    # web_scrapper = WebScrapper(parent_ip=os.environ['MASTER_IP'])
    web_scrapper = WebScrapper(parent_ip="127.0.0.1:8000")

    web_scrapper.scrap_url()
