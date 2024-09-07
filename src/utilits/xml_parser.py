import xml.etree.ElementTree as ET
import os
from src.feed_class.news_feed_parent import NewsFeed
from src.feed_class.news import News
from src.feed_class.private_ad import PrivateAd
from src.feed_class.currency_conv import CurrencyConversion
from src.utilits.text_functions import convert_to_normalized_case
from src.utilits.db_connection import DBConnection


class XmlParser:
    def __init__(self, file_name):
        """Initialize a XmlParser instance.

        Args:
        file_name (str): The name of the XML file to parse."""
        self.file_name = file_name
        self.full_path = None
        self.source_xml = None
        self.path = None

    def load_from_xml(self, path):
        """Load XML content from a file.

        Args:
        path (str): The path to the XML file."""
        self.path = path
        self.full_path = os.path.join(self.path, self.file_name)
        self.source_xml = ET.parse(f'{self.full_path}')

    def parse_from_xml(self):
        """Parse and process XML content."""

        root = self.source_xml.getroot()
        found_valid_transaction = False
        found_invalid_transaction = False

        if root.tag == 'data':
            for transaction in root.findall('transaction'):
                operation_type = transaction.find('operation_type').text
                if operation_type == 'news':
                    news_feed = NewsFeed('news')
                    news_feed = News(convert_to_normalized_case(transaction.find('input_text').text),
                                            convert_to_normalized_case(transaction.find('city').text))
                    news_feed.add_publication()
                    found_valid_transaction = True
                    db_record = DBConnection('new_db')
                    db_record.db_create('news', db_record.columns_news)
                    db_record.db_insert('news', "input_text, city, date",
                                        f"""'{news_feed.input_text}',
                                        '{news_feed.city}',
                                        '{news_feed.date}'""")
                elif operation_type == 'private advertisement':
                    news_feed = NewsFeed('private advertisement')
                    news_feed = PrivateAd(convert_to_normalized_case(transaction.find('input_text').text),
                                                 (transaction.find('expir_date').text))
                    news_feed.add_publication()
                    found_valid_transaction = True
                    db_record = DBConnection('new_db')
                    db_record.db_create('private_ad', db_record.columns_private_ad)
                    db_record.db_insert('private_ad', "input_text, expir_date, days_left",
                                        f"""'{news_feed.input_text}',
                                        '{news_feed.expir_date}',
                                        '{news_feed.days_left}'""")
                elif operation_type == 'currency_conversion':
                    news_feed = NewsFeed('currency_conversion')
                    news_feed = CurrencyConversion(convert_to_normalized_case(transaction.find('from_currency').text),
                                                          convert_to_normalized_case(transaction.find('to_currency').text),
                                                          transaction.find('exchange_rate').text,
                                                          convert_to_normalized_case(transaction.find('city').text))
                    news_feed.add_publication()
                    found_valid_transaction = True
                    db_record = DBConnection('new_db')
                    db_record.db_create('currency_conv', db_record.columns_currency_conv)
                    db_record.db_insert('currency_conv', "currency_from, currency_to, rate, city, date",
                                        f"""'{news_feed.currency_from}',
                                         '{news_feed.currency_to}',
                                         '{news_feed.rate}',
                                         '{news_feed.city}',
                                         '{news_feed.date}'""")
                else:
                    print(f'Invalid record: {operation_type}. Please check the file.')
                    found_invalid_transaction = True

        if not found_valid_transaction or found_invalid_transaction:
            print("Invalid record structure of the file. Please check the file.")
        else:
            try:
                os.remove(self.full_path)
            except FileNotFoundError:
                pass
