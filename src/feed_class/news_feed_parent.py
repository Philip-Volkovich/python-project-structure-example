class NewsFeed:
    def __init__(self, operation_type):
        """Initialize a NewsFeed instance.

        Args:
            operation_type (str): The type of operation (e.g., 'news', 'private advertisement',
            'currency conversion rate').
        """
        self.operation_type = operation_type
        self.record = None

    def add_publication(self):
        """Add the record to a text file and print a success message."""
        with open('news_feed.txt', 'a') as file:
            file.write(self.record.publish())
            file.write('\n\n')
            print(f'Your {self.operation_type} was successfully published ')