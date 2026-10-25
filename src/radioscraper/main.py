from io import StringIO
from typing import List

from radioscraper.http_layer import EibiAPI
from radioscraper.parser import EibiParser, readme_language_code_extract_to_json
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
    with open(settings.EIBI_README_FILE, 'r') as f:
        readme_language_code_extract_to_json(f)



    ## Station parser
    parser = EibiParser(fn=settings.CSV_FILE)
    broadcast = parser.parse_file()

    #GUI

if __name__ == '__main__':
    main()