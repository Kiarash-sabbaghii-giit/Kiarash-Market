from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from db_config import get_collection

collection = get_collection("snacks")



options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.okala.com/store/8875/browse/refreshments?rootId=1467")
time.sleep(5)

# اسکرول تا انتهای صفحه برای لود همه محصولات
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_attempts = 0
while scroll_attempts < 10:  # حداکثر 10 بار اسکرول
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    scroll_attempts += 1
    print(f"اسکرول {scroll_attempts}...")

# حالا همه المنت‌ها رو بگیر
all_names = driver.find_elements(By.CSS_SELECTOR, "p.typo-body-5")
all_prices = driver.find_elements(By.CSS_SELECTOR, "p.body-price-tag")
all_images = driver.find_elements(By.TAG_NAME, "img")

print(f"\n🔍 تعداد اسم‌ها: {len(all_names)}")
print(f"🔍 تعداد قیمت‌ها: {len(all_prices)}")
print(f"🔍 تعداد عکس‌ها: {len(all_images)}")

products = []
seen_names = set()  # برای جلوگیری از تکراری

for i, name_elem in enumerate(all_names):
    name = name_elem.text.strip()

    # فیلتر: اسم نباید عدد خالص باشه
    if name.replace(',', '').replace('٬', '').replace('۰', '').replace('۱', '').replace('۲', '').isdigit():
        continue

    # جلوگیری از تکرار
    if name in seen_names:
        continue
    seen_names.add(name)

    # پیدا کردن قیمت
    price = "ناموجود"
    if i < len(all_prices):
        price = all_prices[i].text

    # پیدا کردن عکس (با روش دقیق‌تر)
    img_url = ""

    # روش 1: اگه عکس alt داره با اسم مطابقت داره
    for img in all_images:
        alt = img.get_attribute("alt") or ""
        if name in alt or alt in name:
            img_url = img.get_attribute("src")
            break

    # روش 2: اگه پیدا نشد، از عکس همون ایندکس استفاده کن
    if not img_url and i < len(all_images):
        img_url = all_images[i].get_attribute("src") or ""

    # روش 3: اگه بازم نشد، از عکس نزدیک از نظر موقعیت استفاده کن
    if not img_url:
        try:
            parent = name_elem.find_element(By.XPATH, "./ancestor::div[.//img]")
            img_url = parent.find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            img_url = "عکس موجود نیست"

    products.append({
        "name": name,
        "price": f"{price} تومان" if price != "ناموجود" else price,
        "image_url": img_url,
        "store": "ارغوان"
    })

    print(f"✅ {len(products)}. {name} : {price} تومان")

driver.quit()

# ذخیره در MongoDB
collection.delete_many({})
if products:
    collection.insert_many(products)
    print(f"\n🎉 {len(products)} محصول با عکس در دیتابیس ذخیره شد.")
else:
    print("❌ محصولی پیدا نشد")

# آمار نهایی
print("\n--- آمار نهایی ---")
print(f"تعداد کل محصولات ذخیره شده: {collection.count_documents({})}")

# نمایش چند نمونه
print("\n--- نمونه محصولات ---")
for item in collection.find().limit(5):
    print(f"• {item['name'][:50]}... | {item['price']}")
# برای دیدن تعداد محصولات
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.okala.com/store/8875/browse/refreshments?rootId=1467")
time.sleep(5)

# اسکرول تا انتها
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# تعداد محصولات واقعی
all_names = driver.find_elements(By.CSS_SELECTOR, "p.typo-body-5")
real_products = [name.text for name in all_names
                 if not name.text.replace(',', '').replace('٬', '').replace('۰', '').isdigit()]

print(f"تعداد کل محصولات واقعی در بخش تنقلات: {len(real_products)}")

driver.quit()
"""