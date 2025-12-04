from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

print("Defining Settings class...")


class TestSettings(BaseSettings):
    foo: str = Field("bar")
    model_config = SettingsConfigDict(env_file=".env")


print("Instantiating Settings...")
settings = TestSettings()
print(f"Loaded: {settings.foo}")
