
from pydantic_settings import BaseSettings
from pydantic import Field

print("Defining Settings class...")
class TestSettings(BaseSettings):
    foo: str = Field("bar")
    
    class Config:
        env_file = ".env"

print("Instantiating Settings...")
settings = TestSettings()
print(f"Loaded: {settings.foo}")
