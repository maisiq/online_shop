from django.conf import settings
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CDEKSettings(BaseSettings):
    ACCOUNT: str
    PASSWORD: str
    API_URL: str = "https://api.cdek.ru/v2/deliverypoints?type=PVZ&country_code=RU"
    SUGGEST_CITIES_URL: str = 'https://api.edu.cdek.ru/v2/location/suggest/cities?name={}'

    @computed_field
    @property
    def API_TOKEN_URL(self) -> str:
        return (
            f'https://api.edu.cdek.ru/v2/oauth/token?'
            f'grant_type=client_credentials&'
            f'client_id={self.ACCOUNT}&'
            f'client_secret={self.PASSWORD}&'
        )

    model_config = SettingsConfigDict(
        env_prefix='CDEK_',
        env_file=(settings.BASE_DIR / '.env'),
        env_file_encoding='utf-8',
        extra='ignore',
    )


cdek_settings = CDEKSettings()
