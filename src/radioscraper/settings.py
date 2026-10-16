class Settings():

    STREAM_SITE_URL:str = 'http://websdr.ewi.utwente.nl:8901/?tune=1234am'
    SHORT_WAVE_URL:str = 'https://www.short-wave.info/index.php'
    STATION_DB_URL: str = 'http://www.eibispace.de/dx/sked-a26.csv'


settings = Settings() # type:ignore [call-arg]