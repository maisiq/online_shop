from django.conf import settings
from pydantic_settings import BaseSettings, SettingsConfigDict


class StripeConfig(BaseSettings):
    API_KEY: str

    model_config = SettingsConfigDict(
        env_prefix='STRIPE_',
        env_file=(settings.BASE_DIR / '.env'),
        extra='ignore',
    )

stripe_config = StripeConfig()