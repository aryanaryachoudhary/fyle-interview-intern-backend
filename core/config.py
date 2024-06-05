class Config:
    # Your common configuration goes here
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./store.sqlite3'  # production database

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # test database
