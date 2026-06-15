from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from db_config import get_collection

collection = get_collection("drinks")



options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.okala.com/store/8875/browse/beverages?rootId=1465")
time.sleep(5)

# اسکرول تا انتها
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

# پیدا کردن همه کارت‌های محصول
product_cards = driver.find_elements(By.XPATH, "//div[.//p[contains(@class, 'typo-body-5')] and .//img]")

print(f"\n📊 تعداد کل کارت‌های محصول پیدا شده: {len(product_cards)}")

products = []
seen_names = set()

for card in product_cards:
    try:
        # گرفتن اسم
        name_elem = card.find_element(By.CSS_SELECTOR, "p.typo-body-5")
        name = name_elem.text.strip()

        # رد کردن اسم‌های عددی
        if name.replace(',', '').replace('٬', '').replace(' ', '').isdigit():
            continue

        # جلوگیری از تکرار
        if name in seen_names:
            continue
        seen_names.add(name)

        # گرفتن قیمت (اگه داخل کارت هست)
        price = "ناموجود"
        try:
            price_elem = card.find_element(By.CSS_SELECTOR, "p.body-price-tag")
            price = price_elem.text.strip()
        except:
            pass  # اگه قیمت نداشت، بذار "ناموجود"

        # گرفتن عکس
        img_elem = card.find_element(By.TAG_NAME, "img")
        img_url = img_elem.get_attribute("src")

        products.append({
            "name": name,
            "price": f"{price} تومان" if price != "ناموجود" else price,
            "image_url": img_url,
            "store": "ارغوان",
            "category": "نوشیدنی",
            "stock": 100
        })

        print(f"✅ {len(products):3d}. {name[:45]} | {price} تومان")

    except Exception as e:
        continue

driver.quit()

# ذخیره در MongoDB
collection.delete_many({})
if products:
    collection.insert_many(products)
    print(f"\n🎉 {len(products)} محصول از بخش نوشیدنی در دیتابیس ذخیره شد.")

    print(f"\n📊 آمار نهایی:")
    print(f"تعداد کل محصولات: {collection.count_documents({})}")

    print("\n📋 ۵ نمونه اول:")
    for item in collection.find().limit(5):
        print(f"  • {item['name'][:35]} | {item['price']}")
else:
    print("❌ محصولی پیدا نشد")