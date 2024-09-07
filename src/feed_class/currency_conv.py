from src.feed_class.news_feed_parent import NewsFeed
from datetime import date, datetime

class CurrencyConversion(NewsFeed):
    def __init__(self, currency_from, currency_to, rate, city):
        """Initialize a Currency Conversion Rate record.

        Args:
            currency_from (str): The currency code to convert from (e.g., 'USD').
            currency_to (str): The currency code to convert to (e.g., 'EUR').
            rate (float): The currency exchange rate.
            city (str): The city associated with the exchange rate.
        """
        super().__init__('currency conversion rate')
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.rate = rate
        self.city = city
        self.date = datetime.now().strftime('%Y-%m-%d, %H:%M')

    def publish(self):
        """Format and return the currency conversion rate record as a string.

        Returns:
            str: The formatted currency conversion rate record.
        """
        return f''' CurrencyConversion--------------
 Todays rate: 1 {self.currency_from} = {self.rate} {self.currency_to}
 {self.city}, {self.date}
        '''