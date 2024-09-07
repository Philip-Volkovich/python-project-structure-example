import sys
import os
from src.feed_class.news import News
from src.feed_class.currency_conv import CurrencyConversion
from src.feed_class.private_ad import PrivateAd
from src.utilits.source_parser import TextParser
from src.utilits.csv_creator import CsvCreator
from src.utilits.json_parser import JsonParser
from src.utilits.xml_parser import XmlParser
from src.utilits.db_connection import DBConnection


class AppRunner:

    def __init__(self):
        self.source_files = 'src/source_files'

    def console_runner(self):
        """Run the console-based news feed application."""

        while True:
            print("\nSelect the way you want add data:")
            print("1. Console mode")
            print("2. Load from txt")
            print("3. Load from json")
            print("4. Load from xml")
            print("5. Exit")
            main_choice = input("Enter your choice: ")

            if main_choice == '1':
                while True:
                    print("\nSelect type of record to add:")
                    print("1. News")
                    print("2. Private Advertisement")
                    print("3. Currency Rate")
                    print("4. Exit")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        input_text = input('Enter the news text: ')
                        city = input('Enter the news city: ')
                        news_feed = News(input_text, city)
                        news_feed.add_publication()
                        db_record = DBConnection('new_db')
                        db_record.db_create('news',db_record.columns_news)
                        db_record.db_insert('news',"input_text, city, date",
                                            f"""'{news_feed.input_text}',
                                            '{news_feed.city}',
                                            '{news_feed.date}'""")
                        csv_creator = CsvCreator(os.getcwd())
                        csv_creator.word_counter()
                        csv_creator.letter_count()
                    elif choice == '2':
                        input_text = input('Enter the private advertisement text: ')
                        expir_date = input('Enter expiration date (YYYY-MM-DD): ')
                        news_feed = PrivateAd(input_text, expir_date)
                        news_feed.add_publication()
                        db_record = DBConnection('new_db')
                        db_record.db_create('private_ad',db_record.columns_private_ad)
                        db_record.db_insert('private_ad',"input_text, expir_date, days_left",
                                            f"""'{news_feed.input_text}',
                                            '{news_feed.expir_date}',
                                            '{news_feed.days_left}'""")
                        csv_creator = CsvCreator(os.getcwd())
                        csv_creator.word_counter()
                        csv_creator.letter_count()
                    elif choice == '3':
                        currency_from = input('Enter FROM which currency you want to convert (3 capital letters, e.g., USD): ')
                        currency_to = input('Enter TO which currency you want to convert (3 capital letters, e.g., USD): ')
                        rate = float(input('Enter currency exchange rate (integer or decimal): '))
                        city = input('Enter city for currency exchange rate: ')
                        news_feed = CurrencyConversion(currency_from, currency_to, rate, city)
                        news_feed.add_publication()
                        db_record = DBConnection('new_db')
                        db_record.db_create('currency_conv',db_record.columns_currency_conv)
                        db_record.db_insert('currency_conv',"currency_from, currency_to, rate, city, date",
                                            f"""'{news_feed.currency_from}',
                                            '{news_feed.currency_to}',
                                            '{news_feed.rate}',
                                            '{news_feed.city}',
                                            '{news_feed.date}'""")
                        csv_creator = CsvCreator(os.getcwd())
                        csv_creator.word_counter()
                        csv_creator.letter_count()
                    elif choice == '4':
                        print("Exiting the console mode.")
                        break
                    else:
                        print('Invalid choice. Please select a valid option.')
            elif main_choice == '2':
                file_name = input("Enter the name of the text file: ")
                file_path = input('''Enter the path of the text file ends with file folder name
                                  (press Enter for default path):''').strip()

                if not file_path:
                    file_path = os.path.join(os.getcwd(), self.source_files)

                full_file_path = os.path.join(file_path, file_name)

                if os.path.exists(full_file_path):
                    text_parser = TextParser(file_name)
                    text_parser.parse_from_text(file_path)
                    text_parser.line_parser()
                    csv_creator = CsvCreator(os.getcwd())
                    csv_creator.word_counter()
                    csv_creator.letter_count()
                else:
                    print(
                        f"The specified file '{full_file_path}' does not exist. Please provide a valid file path.")

            elif main_choice == '3':
                file_name = input("Enter the name of the JSON file: ")
                file_path = input('''Enter the path of the JSON file ends with file folder name
                                  (press Enter for default path):''').strip()

                if not file_path:
                    file_path = os.path.join(os.getcwd(), self.source_files)

                full_file_path = os.path.join(file_path, file_name)

                if os.path.exists(full_file_path):
                    json_parser = JsonParser(file_name)
                    json_parser.load_from_json(file_path)
                    json_parser.parse_from_json()
                    csv_creator = CsvCreator(os.getcwd())
                    csv_creator.word_counter()
                    csv_creator.letter_count()
                else:
                    print(
                        f"The specified file '{full_file_path}' does not exist. Please provide a valid file path.")

            elif main_choice == '4':
                file_name = input("Enter the name of the XML file: ")
                file_path = input('''Enter the path of the XML file ends with file folder name
                                  (press Enter for default path):''').strip()

                if not file_path:
                    file_path = os.path.join(os.getcwd(), self.source_files)

                full_file_path = os.path.join(file_path, file_name)

                if os.path.exists(full_file_path):
                    xml_parser = XmlParser(file_name)
                    xml_parser.load_from_xml(file_path)
                    xml_parser.parse_from_xml()
                    csv_creator = CsvCreator(os.getcwd())
                    csv_creator.word_counter()
                    csv_creator.letter_count()
                else:
                    print(
                        f"The specified file '{full_file_path}' does not exist. Please provide a valid file path.")

            elif main_choice == '5':
                print('Exiting the program')
                break

if __name__ == "__main__":
    run_app = AppRunner()
    run_app.console_runner()
