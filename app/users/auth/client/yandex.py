
from dataclasses import dataclass
import httpx
from app.users.auth.schema import GoogleUserData, YandexUserData
from app.settings import Settings


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str):
        access_token = await self._get_access_token(code)

        async with self.async_client as client:
            headers = {
                "Authorization": f"OAuth {access_token}"
            }

            
            user_info = await client.get("https://login.yandex.ru/info", headers=headers)


        return YandexUserData(**user_info.json(), access_token=access_token)

        

    async def _get_access_token(self, code: str) -> str:

        async with self.async_client as client:
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.settings.YANDEX_CLIENT_ID,
                "client_secret": self.settings.YANDEX_CLIENT_SECRET,
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            response = await client.post(self.settings.YANDEX_TOKEN_URL, data=data, headers=headers)

        print("Token response status:", response.status_code)
        print("Token response text:", response.text)

        response.raise_for_status()
        return response.json().get("access_token")

 