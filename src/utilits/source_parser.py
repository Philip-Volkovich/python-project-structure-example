import os
from src.feed_class.news_feed_parent import NewsFeed
from src.feed_class.news import News
from src.feed_class.private_ad import PrivateAd
from src.feed_class.currency_conv import CurrencyConversion
from src.utilits.text_functions import convert_to_normalized_case
from src.utilits.db_connection import DBConnection

class TextParser:
    def __init__(self, file_name):
        """Initialize a TextParser instance.

        Args:
        file_name (str): The name of the text file to parse."""
        self.file_name = file_name
        self.path = None
        self.full_path = None
        self.parsed_content = None

    def parse_from_text(self, path=None):
        """Parse content from a text file.

        Args:
            path (str, optional): The path to the text file. Defaults to None.
        """
        self.path = path
        self.full_path = os.path.join(self.path, self.file_name)

        with open(f'{self.full_path}', 'r') as file:
            parsed_content = file.read().strip()
            self.parsed_content = parsed_content.split('/')

    def line_parser(self):
        """Parse and process each line of content from the file."""

        for record_str in self.parsed_content:
            record_dict = {}
            pairs_list = record_str.strip().split(';')
            for pair in pairs_list:
                pair = pair.strip().split(':')
                if len(pair) == 2:
                    key = pair[0].strip()
                    value = pair[1].strip()
                    record_dict[key] = value
                    operation_type = record_dict.get('operation_type')

            if (operation_type == 'news'):
                news_feed = NewsFeed('news')
                news_feed = News(convert_to_normalized_case(record_dict.get('input_text')),
                                        convert_to_normalized_case(record_dict.get('city')))
                news_feed.add_publication()
                db_record = DBConnection('new_db')
                db_record.db_create('news', db_record.columns_news)
                db_record.db_insert('news', "input_text, city, date",
                                    f"""'{news_feed.input_text}',
                                     '{news_feed.city}',
                                     '{news_feed.date}'""")

            elif operation_type == 'private advertisement':
                news_feed = NewsFeed('private advertisement')
                news_feed = PrivateAd(convert_to_normalized_case(record_dict.get('input_text')),
                                             record_dict.get('expir_date'))
                news_feed.add_publication()
                db_record = DBConnection('new_db')
                db_record.db_create('private_ad', db_record.columns_private_ad)
                db_record.db_insert('private_ad', "input_text, expir_date, days_left",
                                    f"""'{news_feed.input_text}',
                                    '{news_feed.expir_date}',
                                    '{news_feed.days_left}'""")
            elif operation_type == 'currency_conversion':
                news_feed = NewsFeed('currency_conversion')
                news_feed = CurrencyConversion(convert_to_normalized_case(record_dict.get('from_currency')),
                                                      convert_to_normalized_case(record_dict.get('to_currency')),
                                                      record_dict.get('exchange_rate'),
                                                      convert_to_normalized_case(record_dict.get('city')))
                news_feed.add_publication()
                db_record = DBConnection('new_db')
                db_record.db_create('currency_conv', db_record.columns_currency_conv)
                db_record.db_insert('currency_conv', "currency_from, currency_to, rate, city, date",
                                    f"""'{news_feed.currency_from}',
                                    '{news_feed.currency_to}',
                                    '{news_feed.rate}',
                                    '{news_feed.city}',
                                    '{news_feed.date}'""")
            else:
                print(f'Invalid record: {record_str}. Please check the file.')

            try:
                os.remove(self.full_path)
            except FileNotFoundError:
                pass


