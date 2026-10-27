from io import StringIO
from typing import List

from radioscraper.http_layer import EibiAPI
from radioscraper.parser import EibiParser, LanguageCodesParser
from radioscraper.settings import settings
import os


def main() -> None:
    eibiAPI = EibiAPI()

    if not os.path.exists(settings.CSV_FILE):
        bytes_data = eibiAPI.get_station_data()
        eibiAPI.write_data_to_csv(settings.CSV_FILE, bytes_data)

    if not os.path.exists(settings.EIBI_README_FILE):
        eibiAPI.write_readme()


    #Parsers
    ## Readme parser
    code_parser = LanguageCodesParser()
    with open(settings.EIBI_README_FILE, 'r', encoding='utf-8') as f:
        code_parser(f)






    ## Station parser
    parser = EibiParser(fn=settings.CSV_FILE)
    broadcast = parser.parse_file()
    print(broadcast)

    #GUI

if __name__ == '__main__':
    main()