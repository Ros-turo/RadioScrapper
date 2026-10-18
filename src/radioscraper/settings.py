class Settings():

    STREAM_SITE_URL:str = 'http://websdr.ewi.utwente.nl:8901/?tune=1234am'
    SHORT_WAVE_URL:str = 'https://www.short-wave.info/index.php'
    EIBI_URL: str = 'http://www.eibispace.de/dx/sked-a26.csv'
    CSV_FILENAME: str = "eibi.csv"


settings = Settings() # type:ignore [call-arg]