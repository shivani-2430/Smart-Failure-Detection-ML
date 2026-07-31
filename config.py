import os

class Config:

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:Root%40123@localhost:5432/smart_failure_detection"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False