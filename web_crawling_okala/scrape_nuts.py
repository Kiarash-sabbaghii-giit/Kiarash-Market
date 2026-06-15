from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from db_config import get_collection

collection = get_collection("nuts")

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.okala.com/store/8875/browse/nuts-sweets?rootId=1468")
time.sleep(5)

# گرفتن مستقیم اطلاعات از روی صفحه
try:
    # محصول اول (۲۵۰ گرمی)
    name1 = "مغز گردو ایرانی 250 گرمی"
    price1 = "۵۰۰٬۰۰۰"
    img1 = "https://asset.okala.com/unsigned/rs:fill/size:142:142/quality:90/f:jpg/dpr:1/plain/s3://cdn/product/424991.png"

    # محصول دوم (۵۰۰ گرمی)
    name2 = "مغز گردو ایرانی 500 گرمی"
    price2 = "۱٬۰۰۰٬۰۰۰"
    img2 = "https://asset.okala.com/unsigned/rs:fill/size:142:142/quality:90/dpr:1/plain/s3://cdn/product/0098f4c6-d5ac-4990-beca-ef429e8dde52.jpg"

    products = [
        {
            "name": name1,
            "price": f"{price1} تومان",
            "image_url": img1,
            "store": "ارغوان",
            "category": "آجیل و خشکبار",
            "stock": 100
        },
        {
            "name": name2,
            "price": f"{price2} تومان",
            "image_url": img2,
            "store": "ارغوان",
            "category": "آجیل و خشکبار",
            "stock": 100
        }
    ]

    collection.delete_many({})
    collection.insert_many(products)
    print(f"🎉 {len(products)} محصول با موفقیت ذخیره شد.")

except Exception as e:
    print(f"خطا: {e}")

driver.quit()