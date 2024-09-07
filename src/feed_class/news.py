from src.feed_class.news_feed_parent import NewsFeed
from datetime import date, datetime

class News(NewsFeed):
    def __init__(self, input_text, city):
        """Initialize a News record.

        Args:
            input_text (str): The news text.
            city (str): The city associated with the news.
        """
        super().__init__('news')
        self.input_text = input_text
        self.city = city
        self.date = datetime.now().strftime('%Y-%m-%d, %H:%M')

    def publish(self):
        """Format and return the news record as a string.

        Returns:
            str: The formatted news record.
        """
        return f''' News------------------
 {self.input_text} 
 {self.city}. {self.date}
        '''


