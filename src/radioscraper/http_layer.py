import requests

from radioscraper.settings import settings

class StationAPI:

    def __init__(self):
        self.station_url = settings.STATION_DB_URL

    def get_data(self):
        response = requests.get(self.station_url)
        response.raise_for_status()

        with open("stations.csv", "wb") as f:
            f.write(response.content)
