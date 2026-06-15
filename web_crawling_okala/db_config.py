# db_config.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# بارگذاری .env
load_dotenv()

# خواندن تنظیمات
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "okala_db")

# اتصال به دیتابیس (یک بار در کل برنامه)
_client = None

def get_db():
    """دریافت اتصال دیتابیس"""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client[MONGO_DATABASE]

def get_collection(collection_name):
    """دریافت کالکشن مورد نظر"""
    db = get_db()
