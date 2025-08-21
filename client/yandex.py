
from dataclasses import dataclass
import requests
from schema import GoogleUserData, YandexUserData
from settings import Settings


@dataclass
class YandexClient:
    settings: Settings

    def get_user_info(self, code: str):
        access_token = self._get_access_token(code)

        headers = {
            "Authorization": f"OAuth {access_token}"
        }

        user_info = requests.get("https://login.yandex.ru/info", headers=headers)


        return YandexUserData(**user_info.json(), access_token=access_token)

        

    def _get_access_token(self, code: str) -> str:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.settings.YANDEX_CLIENT_ID,
            "client_secret": self.settings.YANDEX_CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(self.settings.YANDEX_TOKEN_URL, data=data, headers=headers)

        print("Token response status:", response.status_code)
        print("Token response text:", response.text)

        response.raise_for_status()
        return response.json().get("access_token")

 