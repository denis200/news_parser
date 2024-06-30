import time
import requests
import logging
from bs4 import BeautifulSoup

from base import ParserBase


class RiaNewsBS4Parser(ParserBase):
    """RIA News BS4 parser class."""
    base_url: str = 'https://ria.ru'

    def __init__(self) -> None:
        self._get_page_html()

    def _get_page_html(self):
        """ Load page html"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logging.error(f"Error fetching {self.base_url}: {str(e)}")

    def _parse_news(self):
        """
        Load the latest news by specified categories with BS4.

        Args:
            categories: Category news titles.

        Returns:
            Dict with news data.
        """
        news = []
        categories = self.soup.find_all(
            'a', class_='cell-extension__item-link'
        )[:5]
        for category in categories:
            category_title = category.find('span').contents[0]
            response = requests.get(f'{self.base_url}{category["href"]}')
            if response.status_code != 200:
                logging.error(f"Error fetching category {category['href']}")
            category_html = BeautifulSoup(response.text, 'html.parser')
            news_element = category_html.find('a', class_='list-item__title')
            if not news_element:
                logging.error(f'Error loading the news. Category {category}')
            news.append({
                'category': category_title,
                'title': news_element.contents[0],
                'link': news_element['href']
            })
            time.sleep(1)
        if news:
            self._save_news_to_csv(news, 'requests')
        return news
