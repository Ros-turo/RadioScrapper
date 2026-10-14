import datetime

from radioscraper.station_scrapper import StationScrapper, FormData
from radioscraper.settings import settings

def test_scrapper_init() -> None:
    scrapper = StationScrapper(url=settings.SHORT_WAVE_URL)
    assert scrapper.url == settings.SHORT_WAVE_URL

def test_form_data_instance() -> None:
    form_data = FormData()
    assert form_data.station == "Any Station"
    assert form_data.language == "Any Language"
    assert form_data.GMT == True
    assert form_data.submit == "GO"
    assert form_data.mobile == False

def test_form_data_raw() -> None:
    form_data = FormData()
    now, now2 = form_data.get_now()
    assert form_data.raw_json() == f"station=Any+Station&language=Any+Language&now={now}&now2={now2}&GMT=true&submit=GO&mobile=false"
