import logging
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from base import ParserBase


DEFAULT_CATEGORIES: list[str] = [
    'Политика', 'В мире', 'Экономика', 'Общество', 'Происшествия'
]


class RIANewsSeleniumParser(ParserBase):
    """RIA News Selenium parser class."""
    base_url: str = 'https://ria.ru/'

    def __init__(self) -> None:
        self._init_driver()

    def _init_driver(self) -> None:
        """
        Init selenium ChromeDriver.
        """
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=chrome_options
        )

    def _process_news(
        self,
        news_item: WebElement,
        category: str
    ) -> dict[str, str]:
        """
        Load data from the news page.

        Args:
            news_item: News title WeblElement.
            category: The name of the news category.

        Returns:
            Dict with news data.
        """
        news_title = news_item.text
        news_link = news_item.get_attribute('href')
        self.driver.get(news_link)
        time.sleep(2)
        news_describtion = self.driver.find_element(
            By.CSS_SELECTOR, '.article__text'
        ).text
        self.driver.back()
        return {
            'category': category,
            'title': news_title,
            'link': news_link,
            'description': news_describtion,
        }

    def _parse_news(self, categories: list[str] = DEFAULT_CATEGORIES):
        """
        Load the latest news by specified categories with Selenium.

        Args:
            categories: Category news titles.

        Returns:
            Dict with news data.
        """
        news = []
        self.driver.get(self.base_url)
        time.sleep(3)
        for category in categories:
            try:
                category_page = self.driver.find_element(
                    By.LINK_TEXT, category
                )
            except NoSuchElementException:
                logging.error(f"Category {category} not found")
                continue
            category_page.click()
            time.sleep(2)
            news_item = self.driver.find_element(
                By.CSS_SELECTOR, '.list-item__title'
            )
            try:
                news_data = self._process_news(news_item, category)
            except Exception as e:
                logging.error(
                    f"An error occurred while processing the news: {e}"
                )
            if news_data:
                news.append(news_data)
            self.driver.back()
            time.sleep(2)
        if news:
            self._save_news_to_csv(news, 'selenium')
        return news
