import pytest

from radioscraper.http_layer import RadioShortWaveSession, ShortWaveFormData


@pytest.fixture
def mozilla_user_agent() -> dict[str,str]:
    return {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0"}


@pytest.fixture
def short_wave_headers(mozilla_user_agent: dict[str,str]) -> dict[str,str]:
    headers = mozilla_user_agent.copy()
    headers.update({
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.short-wave.info",
        "Origin": "https://www.short-wave.info",
        "Referer": "https://www.short-wave.info/",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9"
    })
    return headers

@pytest.fixture
def radio_short_wave_session(short_wave_headers: dict[str,str]) -> RadioShortWaveSession:
    return RadioShortWaveSession(short_wave_headers)

@pytest.fixture
def form_data() -> ShortWaveFormData:
    return ShortWaveFormData()