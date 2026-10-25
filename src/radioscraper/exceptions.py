class InvalidURL(Exception):

    def __init__(self, url):
        super().__init__(f"Invalid URL: {url}")

class NotWeekdayPeriodError(Exception):
    pass