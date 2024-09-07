import csv
import os
import re
from collections import Counter


class CsvCreator:
    def __init__(self, path=None):
        self.default_path = path or os.getcwd()
        self.csv_output = 'csv_output'
        self.output_dir = os.path.join(self.default_path, self.csv_output)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def word_counter(self):
        with open(os.path.join(self.default_path, 'news_feed.txt'), 'r') as file:
            news_feed_file = file.read()
            news_feed_file = news_feed_file.lower()
            # r'\b(?![\d-])\w+\b'
            words = re.findall(r'\b[a-zA-Z\']+\b', news_feed_file)
            words_count = Counter(words)

        with open(os.path.join(self.output_dir, 'word_count.csv'), 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for key, value in words_count.items():
                csv_writer.writerow([f'{key}-{value}'])

    def letter_count(self):
        with open(os.path.join(self.default_path, 'news_feed.txt'), 'r') as file:
            news_feed_file = file.read()
            all_letters = re.findall(r'[a-zA-Z]', news_feed_file)
            count_all_letters = len(all_letters)
            letter_counts = Counter(all_letters)

        with open(os.path.join(self.output_dir, 'letter_count.csv'), 'w', newline='') as csv_file:
            fieldnames = ['letter', 'count_all', 'count_uppercase', 'percentage']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            csv_writer.writeheader()

            for letter in sorted(letter_counts.keys()):
                count_uppercase = sum(1 for l in all_letters if l.isupper() and l == letter)
                percentage = round ((letter_counts[letter] / count_all_letters) * 100,2) if count_all_letters > 0 else 0
                csv_writer.writerow(
                    {'letter': letter, 'count_all': letter_counts[letter], 'count_uppercase': count_uppercase,
                     'percentage': percentage})

