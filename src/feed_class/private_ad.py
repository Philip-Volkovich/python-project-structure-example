from src.feed_class.news_feed_parent import NewsFeed
from datetime import date, datetime

class PrivateAd(NewsFeed):
    def __init__(self, input_text, expir_date):
        """Initialize a Private Advertisement record.

        Args:
            input_text (str): The advertisement text.
            expir_date (str): The expiration date in the format 'YYYY-MM-DD'.
        """
        super().__init__('private advertisement')
        self.input_text = input_text
        self.expir_date = datetime.strptime(expir_date, '%Y-%m-%d').date()
        self.days_left = (self.expir_date - date.today()).days

    def publish(self):
        """Format and return the private advertisement record as a string.

        Returns:
            str: The formatted private advertisement record.
        """
        return f''' PrivateAd--------------
 {self.input_text} 
 Actual until: {self.expir_date}, {self.days_left} days left
        '''