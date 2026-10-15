import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class AppConfig:
    name :str
    base_url : str
    api_url : str
    username : str
    password : str

APPs = { "app_one": AppConfig(
        name="app_one",
        base_url=os.getenv("APP_ONE_URL", "https://www.saucedemo.com"),
        api_url=os.getenv("APP_ONE_API", "https://jsonplaceholder.typicode.com"),
        username=os.getenv("APP_ONE_USER", "standard_user"),
        password=os.getenv("APP_ONE_PASS", "secret_sauce"),
    ),
    "app_two": AppConfig(
        name="app_two",
        base_url=os.getenv("APP_TWO_URL", "http://localhost:3000"),
        api_url=os.getenv("APP_TWO_API", "http://localhost:8000"),
        username=os.getenv("APP_TWO_USER", "demo"),
        password=os.getenv("APP_TWO_PASS", "demo"),
    )}

BROWSER = os.getenv("BROWSER" , "chromium")
HEADLESS = os.getenv("HEADLESS" , "true").lower() == "true"
ARTIFACTS_DIR = Path("artifacts")

