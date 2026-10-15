from radioscraper.http_layer import RadioShortWaveSession, ShortWaveFormData
from radioscraper.settings import settings


def test_create_session(short_wave_headers: dict[str, str]) -> None:
    s = RadioShortWaveSession()
    assert isinstance(s, RadioShortWaveSession)
    assert s.url == settings.SHORT_WAVE_URL

def test_create_session_with_headers(short_wave_headers: dict[str,str]) -> None:
    s = RadioShortWaveSession(headers = short_wave_headers)
    assert short_wave_headers.items() <= s.headers.items()

def test_create_form_data() -> None:
    form_data = ShortWaveFormData()
    assert isinstance(form_data, ShortWaveFormData)
    assert form_data.station == 'Any station'
    assert form_data.language == 'Any language'

def test_form_data_return_dict() -> None:
    form_data = ShortWaveFormData()
    data = form_data()
    assert data['station'] == 'Any station'
    assert data['language'] == 'Any language'


def test_post_request(
        radio_short_wave_session: RadioShortWaveSession,
        form_data: ShortWaveFormData
) -> None:
    response = radio_short_wave_session.get_response_with_now(data=form_data)
    assert response.status_code == 200
