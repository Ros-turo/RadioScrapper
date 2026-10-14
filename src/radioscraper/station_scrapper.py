import datetime
import json
from dataclasses import dataclass


class StationScrapper:

    def __init__(self, url) -> None:
        self.url = url


class FormData:

    def __init__(self) -> None:
        self.station = "Any Station"
        self.language = "Any Language"
        self.GMT = True
        self.submit = "GO"
        self.mobile = False

    def get_now(self) -> tuple:
        now = datetime.datetime.now()
        return now.hour, now.minute


    def raw_json(self) -> str:
        station_raw = self.station.replace(" ", "+")
        language_raw = self.language.replace(" ", "+")
        GMT_raw = json.dumps(self.GMT)
        submit_raw = self.submit
        mobile_raw = json.dumps(self.mobile)
        now, now2 = self.get_now()
        return f"station={station_raw}&language={language_raw}&now={now}&now2={now2}&GMT={GMT_raw}&submit={submit_raw}&mobile={mobile_raw}"