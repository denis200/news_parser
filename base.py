import logging
import pandas as pd


logging.basicConfig(
    filename='errors.log',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


class ParserBase():
    def _save_news_to_csv(
        self,
        news: list[dict[str, str]],
        file_name: str
    ):
        """
        Save news to csv file.

        Args:
            news: List of collected news.
        """
        try:
            pd.DataFrame(news).to_csv(
                f'news_{file_name}.csv',
                index=False,
                encoding='utf-8'
            )
        except Exception as e:
            logging.error(f'An error occurred while saving to a file: {e}')
