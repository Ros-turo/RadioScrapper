import csv
import json
from datetime import  time
import os
from abc import ABC, abstractmethod
from typing import List

from radioscraper.exceptions import NotWeekdayPeriodError
from radioscraper.model import Broadcast, StationData
from radioscraper.settings import settings


class Parser(ABC):

    def __init__(self, fn: str):
        self.fn = self._is_file_exists(fn)

    def _is_file_exists(self, fn: str) -> str:
        if os.path.isfile(fn):
            return fn
        raise FileNotFoundError(fn)

    @abstractmethod
    def parse_file(self) -> Broadcast: ...

    @abstractmethod
    def parse_row(self, row) -> StationData: ...

    @abstractmethod
    def get_time(self, time_row: str) -> tuple[time, time]: ...

    @abstractmethod
    def get_station(self, station_row: str) -> str: ...

    @abstractmethod
    def get_language(self, lng:str) -> List[str] | None: ...

    @abstractmethod
    def get_frequency(self, frequency_row: str) -> float | int: ...

    @abstractmethod
    def get_regularity(self, days_row: str) -> List[int] | str: ...


class EibiParser(Parser):

    def parse_file(self) -> Broadcast:
        broadcast = Broadcast()
        with open(self.fn, encoding='latin-1') as file:
            reader = csv.reader(file, delimiter=';')
            reader.__next__()
            for row in reader:
                station_data = self.parse_row(row)
                broadcast.append_station(station_data)

        return broadcast

    def parse_row(self, row: list) -> StationData:
        frequency = self.get_frequency(row[0])
        start_time, end_time = self.get_time(row[1])
        regularity = self.get_regularity(row[2])
        language = self.get_language(row[5])
        station = self.get_station(row[4])
        return StationData(
            frequency=frequency,
            station=station,
            start_time=start_time,
            end_time=end_time,
            regularity=regularity,
            language=language
        )

    def get_time(self, time_row: str) -> tuple[time, time]:
        start_time, end_time = time_row.split('-')

        start_time = time(int(start_time[:2]), int(start_time[2:]))

        if end_time[:2] == "24":
            end_time = "2359"
        end_time = time(int(end_time[:2]), int(end_time[2:]))

        return start_time, end_time

    def get_station(self, station_row: str) -> str:
        return station_row

    def get_frequency(self, frequency_row: str) -> float | int:
        return float(frequency_row)

    def get_language(self, lng: str) -> List[str] | None:
        if not lng:
            return None

        language_parser = LanguageCodesParser()
        language_codes = language_parser.json_to_dict()
        language_array = lng.split(",")
        language_result = []
        for language_code in language_array:
            language = language_codes.get(language_code, None)
            if language:
                language_result.append(language)
        return language_result




    def get_regularity(self, days_row: str) -> List[int] | str:
        #dayday - 4pismena 2dny
        #Last7 - posledni nedele, today + weekday of 1fs in month(except Sunday, -1) = 28
        EVERY_DAY = [0,1,2,3,4,5,6]

        if not days_row:
            return EVERY_DAY

        if days_row == "Last7":
            return "Last7"

        if len(days_row) == 2:
            try:
                weekday = self.get_weekday_from_string_abb(days_row)
                return [weekday]
            except NotWeekdayPeriodError:
                return "irregular"

        if len(days_row) == 4:
            days = [days_row[:2], days_row[2:]]
            try:
                weekdays = [self.get_weekday_from_string_abb(day) for day in days]
                return sorted(weekdays)
            except NotWeekdayPeriodError:
                return "irregular"

        if len(days_row) == 5:
            period = days_row.split("-")
            if len(period) == 2:
                try:
                    weekdays = [self.get_weekday_from_string_abb(day) for day in period]
                    return [day for day in range(weekdays[0], weekdays[1] + 1)]
                except NotWeekdayPeriodError:
                    return "irregular"


        return "irregular"

    @staticmethod
    def get_weekday_from_string_abb(days_row: str) -> int:
        weekday_dict = {
            "Mo": 1,
            "Tu": 2,
            "We": 3,
            "Th": 4,
            "Fr": 5,
            "Sa": 6,
            "Su": 0
        }
        weekday = weekday_dict.get(days_row, None)
        if weekday is None:
            raise NotWeekdayPeriodError()
        return weekday


class LanguageCodesParser:



    def __call__(self, lines) -> None:
        raw_data = self.raw_language_code_data(lines)
        clear_data = self.language_code_data_cleaner(raw_data)
        self.write_language_code_data_to_json(clear_data)


    def raw_language_code_data(self, lines: list[str]) -> list[str]:
        append_zone = False
        raw_language_data = []
        for line in lines:
            if "-CW   Morse Station" in line:
                append_zone = True
            if "II) Country codes." in line:
                append_zone = False
                break
            if append_zone:
                raw_language_data.append(line)
        return raw_language_data

    def language_code_data_cleaner(self, raw_data: list[str]) -> dict[str, str]:
        clear_data = {}
        for row in raw_data:
            if len(row) - len(row.lstrip(' ')) != settings.README_CODE_INDENT:
                continue
            row = row.rstrip()
            row = row.rsplit("(")[0].rsplit(":")[0].rsplit("=")[0].rsplit("/")[0].split(" ")
            row = [el for el in row if el and el != "program"]
            clear_data[row[0]] = " ".join(row[1:])
        return clear_data


    def write_language_code_data_to_json(self, data: dict[str, str]) -> str:
        with open('language_codes.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
        return 'language_codes.json'

    def json_to_dict(self) -> dict[str, str]:
        with open('language_codes.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data