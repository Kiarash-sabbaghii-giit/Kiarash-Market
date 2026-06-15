from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from db_config import get_collection

collection = get_collection("lifestyle")

# راه‌اندازی Selenium
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.okala.com/store/8875/browse/home-stuff?rootId=1473")
time.sleep(5)

# اسکرول برای لود کامل محصولات
print("⏳ در حال لود همه محصولات...")
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_attempts = 0
while scroll_attempts < 20:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2.5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    scroll_attempts += 1
    print(f"اسکرول {scroll_attempts}...")

# پیدا کردن کارت‌های محصول (همان روش موفق)
product_cards = driver.find_elements(By.XPATH, "//div[.//p[contains(@class, 'typo-body-5')] and .//img]")
print(f"\n📊 تعداد کل کارت‌های محصول پیدا شده: {len(product_cards)}")

products = []
seen_names = set()

for card in product_cards:
    try:
        # گرفتن اسم
        name_elem = card.find_element(By.CSS_SELECTOR, "p.typo-body-5")
        name = name_elem.text.strip()

        # رد کردن اسم‌های عددی (که احتمالاً قیمت هستند)
        if name.replace(',', '').replace('٬', '').replace(' ', '').isdigit():
            continue

        # جلوگیری از تکرار اسم
        if name in seen_names:
            continue
        seen_names.add(name)

        # گرفتن قیمت (اگر در کارت موجود باشد)
        price = "ناموجود"
        try:
            price_elem = card.find_element(By.CSS_SELECTOR, "p.body-price-tag")
            price = price_elem.text.strip()
        except:
            pass

        # گرفتن عکس از داخل همان کارت (تضمینی)
        img_elem = card.find_element(By.TAG_NAME, "img")
        img_url = img_elem.get_attribute("src")

        products.append({
            "name": name,
            "price": price,
            "image_url": img_url,
            "store": "ارغوان",
            "category": "خانه و سبک زندگی",
            "stock": 100
        })
        print(f"✅ {len(products):3d}. {name[:45]} | {price}")

    except Exception as e:
        print(f"⚠️ خطا در پردازش یک کارت: {e}")
        continue

driver.quit()

# ذخیره در MongoDB
if products:
    collection.delete_many({})
    collection.insert_many(products)
    print(f"\n🎉 {len(products)} محصول از بخش خانه و سبک زندگی در دیتابیس ذخیره شد.")

    print(f"\n📊 آمار نهایی:")
    print(f"تعداد کل محصولات: {collection.count_documents({})}")

    # گزارش تعداد محصولات بدون قیمت
    missing_count = collection.count_documents({"price": "ناموجود"})
    if missing_count > 0:
        print(f"⚠️ {missing_count} محصول بدون قیمت (ناموجود) هستند.")

    print("\n📋 ۵ نمونه اول:")
    for item in collection.find().limit(5):
        print(f"  • {item['name'][:35]} | {item['price']}")
else:
    print("❌ هیچ محصولی پیدا نشد.")