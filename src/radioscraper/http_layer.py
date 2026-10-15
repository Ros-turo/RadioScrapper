from datetime import datetime

from requests import Session, Response

from radioscraper.settings import settings


class ShortWaveFormData:
    def __init__(self) -> None:
        self.station = "Any station"
        self.language = "Any language"
        self.GMT = 'true'
        self.submit = "GO"
        self.mobile = 'false'
        self.now = datetime.now()

    def __call__(self) -> dict:
        return {
            'station': self.station,
            'language': self.language,
            'GMT': self.GMT,
            'submit': self.submit,
            'mobile': self.mobile,
            'now': self.now.hour,
            'now2': self.now.minute,
        }

    def actualize_now(self) -> None:
        self.now = datetime.now()


class RadioShortWaveSession(Session):

    def __init__(self, headers: dict | None = None) -> None:
        super().__init__()
        if not headers is None:
            self.headers.update(headers)

        self.url = settings.SHORT_WAVE_URL

    def get_response_with_now(self, data: ShortWaveFormData) -> Response:
        data.actualize_now()
        response = self.post(url = self.url, data=data())
        response.raise_for_status()
        return response