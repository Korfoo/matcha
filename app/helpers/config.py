import os

class Config:
    environment = os.getenv("MATCHA_ENVIRONMENT", "debug")

config = Config()