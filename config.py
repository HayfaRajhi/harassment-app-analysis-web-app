import os

class Config :
    DEBUG=True
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/harassment_analitycs')
    SECRET_KEY = os.getenv('SECRET_KEY','')
