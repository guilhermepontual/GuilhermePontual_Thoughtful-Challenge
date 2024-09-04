import time
from selenium.webdriver.common.keys import Keys
from RPA.Browser.Selenium import Selenium
from datetime import datetime, timedelta
import logging
import re
import os
from utils import get_image_src, contains_money, save_to_excel


class NewsScraper:
    def __init__(self, search_phrase, number_of_months):
        self.search_phrase = search_phrase
        self.number_of_months = number_of_months
        self.browser = Selenium()
        self.base_url = "https://gothamist.com/search"

    def run(self):
        try:
            self.browser.open_available_browser(self.base_url)
            self.search_news()
            news_items = self.extract_news()

            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_file = os.path.join(output_dir, "news_data.xlsx")
            save_to_excel(news_items, output_file)

            logging.info(f"Dados salvos no arquivo {output_file}")

            return news_items
        finally:
            self.browser.close_browser()

    def search_news(self):
        time.sleep(4)
        logging.info(f"Searching for '{self.search_phrase}'")
        search_box = '//input[@class="search-page-input"]'
        self.browser.input_text(search_box, self.search_phrase)
        self.browser.press_keys(search_box, Keys.ENTER)

    def extract_news(self):
        date = None
        news_items = []
        cutoff_date = datetime.now() - timedelta(days=self.number_of_months * 30)
        articles_xpath = '//div[@class="content"]//div[@class="col"]/div/div/div/div/a'
        time.sleep(10)
        articles = self.browser.find_elements(articles_xpath)
        logging.info(f"Found {len(articles)} articles.")
        for index in range(1, 2):
            try:
                article_xpath = f"({articles_xpath})[{index}]"
                self.browser.wait_until_element_is_visible(article_xpath, timeout=120)
                self.browser.click_element(article_xpath)

                self.browser.wait_until_element_is_visible('//div[@class="content"]//div[@class="col"]/h1', timeout=10)

                title = self.browser.get_text('//div[@class="content"]//div[@class="col"]/h1')

                dates = self.browser.find_elements('//div[@class="date-published"]')[1]

                date_str = self.browser.get_text(dates)

                if date_str:
                    date = self.parse_date(date_str)

                description_text = []

                descriptions = self.browser.find_elements('//div[@class="streamfield-paragraph rte-text"]/p')

                for paragraph in descriptions:
                    description_text.append(paragraph.text)

                full_description = ' '.join(description_text)

                images = self.browser.find_elements('//img[@class="image native-image prime-img-class"]')[1]

                image_url = self.browser.get_element_attribute(
                    images, "src")

                print(title, date, full_description, image_url)

                if date and date >= cutoff_date:
                    news_items.append({
                        "title": title,
                        "date": date,
                        "description": full_description,
                        "image_filename": image_url,
                        "search_phrase_count": self.search_phrase_count(title, full_description),
                        "contains_money": contains_money(f"{title} {full_description}")
                    })

                self.browser.go_back()
                self.browser.wait_until_element_is_visible(articles_xpath, timeout=10)

            except Exception as e:
                logging.warning(f"Erro ao tentar clicar no artigo {index}: {e}")

        return news_items

    def parse_date(self, date_str):
        try:
            date_part = date_str.split(' at ')[0].replace('Published ', '').strip()

            date = datetime.strptime(date_part, "%b %d, %Y")

            return date
        except ValueError as e:
            logging.error(f"Erro ao parsear a data: {e}")
            return None

    def search_phrase_count(self, title, description):
        return title.lower().count(self.search_phrase.lower()) + description.lower().count(self.search_phrase.lower())
