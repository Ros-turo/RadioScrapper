from radioscraper.http_layer import EibiAPI
from radioscraper.settings import settings
import os




def main() -> None:
    eibiAPI = EibiAPI()

    if not os.path.exists(settings.CSV_FILE):
        bytes_data = eibiAPI.get_data()
        eibiAPI.write_data_to_csv(settings.CSV_FILE, bytes_data)

    #Parser

    #GUI

if __name__ == '__main__':
    main()