class Settings():

    STREAM_SITE_URL:str = 'http://websdr.ewi.utwente.nl:8901/?tune=1234am'
    SHORT_WAVE_URL:str = 'https://www.short-wave.info/index.php'
    EIBI_URL: str = 'http://www.eibispace.de/dx/sked-a26.csv'
    EIBI_README: str = 'http://www.eibispace.de/dx/README.TXT'
    CSV_FILE:str = "stations.csv"
    EIBI_README_FILE:str = "eibi_readme.txt"

    README_CODE_INDENT: int = 3


settings = Settings() # type:ignore [call-arg]