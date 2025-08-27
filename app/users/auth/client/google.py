from dataclasses import dataclass
import httpx
from app.users.auth.schema import GoogleUserData
from app.settings import Settings


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient


    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = self._get_access_token(code=code)
        async with self.async_client() as client:
            user_info = await client.get('https://www.googleapis.com/oauth2/v1/userinfo',
                                     headers={'Authorization': f'Bearer {access_token}'})
        
        return GoogleUserData(**user_info.json(), access_token=access_token)

        

    async def _get_access_token(self, code: str) -> str:
        data = {
            'code': code,
            'client_id': self.settings.GOOGLE_CLIENT_ID,
            'client_secret': self.settings.GOOGLE_SECRET_KEY,
            'redirect_uri': self.settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
    
        print(f"Request data: {data}")  # ← Логируем что отправляем
        async with self.async_client() as client:
            response = await client.post(self.settings.GOOGLE_TOKEN_URL, data=data)
    
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Text: {response.text}")
    
        try:
            result = response.json()["access_token"]
            print(f"JSON: {result}")
            return result
        except Exception as e:
            print(f"JSON parse error: {e}")
            return {"error": "json_parse_error", "text": response.text}
 