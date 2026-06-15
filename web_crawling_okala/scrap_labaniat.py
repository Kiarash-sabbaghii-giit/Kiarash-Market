from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from db_config import get_collection

collection = get_collection("dairy")



options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.okala.com/store/8875/browse/dairy-products?rootId=1462")
time.sleep(5)

# اسکرول
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# پیدا کردن کارت‌های محصول (هر کارت شامل اسم و قیمت و عکس)
# با یک XPath دقیق‌تر که فقط کارت‌های اصلی رو بگیره
product_cards = driver.find_elements(By.XPATH,
                                     "//div[.//p[contains(@class, 'typo-body-5')] and .//p[contains(@class, 'body-price-tag')] and .//img]")

print(f"📊 تعداد کارت‌های محصول پیدا شده: {len(product_cards)}")

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

        # گرفتن قیمت از داخل کارت
        price_elem = card.find_element(By.CSS_SELECTOR, "p.body-price-tag")
        price = price_elem.text.strip()

        # گرفتن عکس از داخل کارت (تضمینی)
        img_elem = card.find_element(By.TAG_NAME, "img")
        img_url = img_elem.get_attribute("src")

        products.append({
            "name": name,
            "price": f"{price} تومان",
            "image_url": img_url,
            "store": "ارغوان",
            "category": "لبنیات",
            "stock": 100
        })
        print(f"✅ {len(products):2d}. {name[:40]} | {price} تومان")

    except Exception as e:
        continue

driver.quit()

# ذخیره در MongoDB
collection.delete_many({})
if products:
    collection.insert_many(products)
    print(f"\n🎉 {len(products)} محصول از بخش لبنیات ذخیره شد.")

    # حذف تکراری‌ها (اگه باشه)
    pipeline = [
        {"$group": {"_id": "$name", "ids": {"$push": "$_id"}, "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    duplicates = list(collection.aggregate(pipeline))
    for dup in duplicates:
        dup["ids"].pop(0)
        collection.delete_many({"_id": {"$in": dup["ids"]}})

    print(f"📊 تعداد نهایی بعد از حذف تکراری‌ها: {collection.count_documents({})}")
else:
    print("❌ محصولی پیدا نشد - ممکنه ساختار کارت‌ها فرق کنه")