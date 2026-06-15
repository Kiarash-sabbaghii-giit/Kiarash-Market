"""from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from db_config import get_collection

collection = get_collection("grocery")



# راه‌اندازی Selenium
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.okala.com/store/8875/browse/groceries?rootId=1461")
time.sleep(5)

# اسکرول
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# گرفتن همه اسم‌ها و قیمت‌ها
name_elements = driver.find_elements(By.CSS_SELECTOR, "p.typo-body-5")
price_elements = driver.find_elements(By.CSS_SELECTOR, "p.body-price-tag")

print(f"📊 اسم‌ها: {len(name_elements)} | قیمت‌ها: {len(price_elements)}")

# ساختن لیست با موقعیت
names = []
for elem in name_elements:
    names.append({
        "text": elem.text.strip(),
        "y": elem.location['y'],
        "element": elem
    })

prices = []
for elem in price_elements:
    prices.append({
        "text": elem.text.strip(),
        "y": elem.location['y'],
        "element": elem
    })

# جفت کردن: هر اسم با نزدیک‌ترین قیمت از نظر موقعیت
products = []
used_prices = set()

for name in names:
    # رد کردن اسم‌های عددی
    name_text = name["text"]
    if name_text.replace(',', '').replace('٬', '').replace(' ', '').isdigit():
        continue

    # پیدا کردن نزدیک‌ترین قیمت
    closest_price = None
    min_distance = float('inf')

    for i, price in enumerate(prices):
        if i in used_prices:
            continue
        distance = abs(price["y"] - name["y"])
        if distance < min_distance and distance < 200:  # حداکثر فاصله 200 پیکسل
            min_distance = distance
            closest_price = price

    if closest_price:
        used_prices.add(prices.index(closest_price))
        price_text = closest_price["text"]

        # گرفتن عکس
        img_url = ""
        try:
            parent = name["element"].find_element(By.XPATH, "./ancestor::div[.//img]")
            img_url = parent.find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            img_url = "عکس موجود نیست"

        products.append({
            "name": name_text,
            "price": f"{price_text} تومان",
            "image_url": img_url,
            "store": "ارغوان",
            "category": "خواربار",
            "stock": 100
        })

        print(f"✅ {len(products)}. {name_text[:40]} | {price_text}")

        if len(products) >= 53:
            break

# ذخیره
collection.delete_many({})
if products:
    collection.insert_many(products)
    print(f"\n🎉 {len(products)} محصول ذخیره شد.")
else:
    print("❌ محصولی پیدا نشد")

driver.quit()
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from db_config import get_collection

collection = get_collection("grocery")



# راه‌اندازی Selenium
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.okala.com/store/8875/browse/groceries?rootId=1461")
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

# پیدا کردن کارت‌های محصول (همان روش موفق در نوشیدنی‌ها)
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
            pass  # اگر قیمت نبود، همان "ناموجود" بماند

        # گرفتن عکس از داخل همان کارت (تضمینی)
        img_elem = card.find_element(By.TAG_NAME, "img")
        img_url = img_elem.get_attribute("src")

        products.append({
            "name": name,
            "price": price,
            "image_url": img_url,
            "store": "ارغوان",
            "category": "خواربار",
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
    print(f"\n🎉 {len(products)} محصول از بخش خواربار در دیتابیس ذخیره شد.")

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