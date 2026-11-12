import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY','frontend-secret_key') 
    API_BASE_URL = os.getenv('API_BASE_URL','http://localhost:5001')

class DevelopmentConfig(Config):
    DEBUG = True

config = {'development': DevelopmentConfig, 'default': DevelopmentConfig}         
