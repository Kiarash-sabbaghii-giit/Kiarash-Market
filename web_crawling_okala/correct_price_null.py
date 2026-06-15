import random
from db_config import get_collection

# تبدیل عدد انگلیسی به فارسی
def to_persian_number(number):
    english_to_persian = {
        '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
        '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
    }
    return ''.join(english_to_persian.get(digit, digit) for digit in str(number))


# تبدیل عدد به فرمت قیمت فارسی
def format_price(price):
    price_str = str(price)
    # جدا کردن سه رقم سه رقم با ٬
    reversed_price = price_str[::-1]
    parts = [reversed_price[i:i + 3] for i in range(0, len(reversed_price), 3)]
    formatted = '٬'.join(parts)[::-1]
    persian_price = to_persian_number(formatted)
    return f"{persian_price} تومان"




collection = get_collection("protein_bar")



# پیدا کردن محصولات ناموجود
missing_products = collection.find({"price": "ناموجود"})
missing_list = list(missing_products)

print(f"📊 تعداد محصولات ناموجود در بخش چندتایی: {len(missing_list)}")

if missing_list:
    for product in missing_list:
        # قیمت رندوم بین ۱۰۰,۰۰۰ تا ۵۰۰,۰۰۰
        random_price = random.randint(100000, 500000)
        formatted_price = format_price(random_price)

        collection.update_one(
            {"_id": product["_id"]},
            {"$set": {"price": formatted_price, "stock": random.randint(30, 150)}}
        )
        print(f"✅ {product['name'][:35]} -> {formatted_price}")

    print(f"\n🎉 {len(missing_list)} محصول قیمت‌گذاری شدن.")
else:
    print("✅ همه محصولات دارای قیمت هستند.")

# آمار نهایی
total = collection.count_documents({})
print(f"📊 تعداد کل محصولات در کالکشن multiples_products: {total}")