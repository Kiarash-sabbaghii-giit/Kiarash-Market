import pymongo
from django.conf import settings


def get_db():
    """دریافت اتصال به دیتابیس MongoDB"""
    try:
        client = pymongo.MongoClient(settings.MONGODB_URI)
        db = client['okala_db']
        # تست اتصال
        client.admin.command('ping')
        print("✅ MongoDB connected successfully")
        return db
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        return None


def get_categories():
    """دریافت همه دسته‌بندی‌ها از کالکشن categories"""
    db = get_db()
    if db is not None:
        # گرفتن همه دسته‌بندی‌ها بدون فیلد _id
        categories = list(db.categories.find({}, {'_id': 0}))
        return categories
    return []


def get_categories_by_english_names(english_names_list):
    """دریافت دسته‌بندی‌های خاص با فیلتر کردن روی category_en"""
    db = get_db()
    if db is not None:
        categories = list(db.categories.find(
            {'category_en': {'$in': english_names_list}},
            {'_id': 0}
        ))
        return categories
    return []


def get_all_categories_sorted():
    """دریافت همه دسته‌بندی‌ها به ترتیب لیست بالا"""
    db = get_db()
    if db is not None:
        # گرفتن همه دسته‌بندی‌ها
        all_categories = list(db.categories.find({}, {'_id': 0}))

        # مرتب‌سازی بر اساس لیست مورد نظر
        CATEGORY_LIST = [
            "snacks", "spices", "breakfast", "canned_food", "cosmetics",
            "dairy", "drinks", "fruits", "grocery", "home_hygiene",
            "lifestyle", "many", "nuts", "protein_bar", "smokes"
        ]

        # مرتب‌سازی
        sorted_categories = []
        for cat_en in CATEGORY_LIST:
            for cat in all_categories:
                if cat.get('category_en') == cat_en:
                    sorted_categories.append(cat)
                    break

        return sorted_categories
    return []


def get_products_by_category(category_en):
    """دریافت محصولات یک دسته خاص"""
    db = get_db()
    if db is not None and category_en in db.list_collection_names():
        products = list(db[category_en].find({}, {'_id': 0}).limit(20))
        return products
    return []
def get_category_info(category_en):
    """دریافت اطلاعات یک دسته بندی خاص"""
    db = get_db()
    if db is not None:
        category = db.categories.find_one({'category_en': category_en}, {'_id': 0})
        return category
    return None

def get_products_by_category(category_en, limit=None):
    """دریافت محصولات یک دسته خاص"""
    db = get_db()
    if db is not None and category_en in db.list_collection_names():
        query = db[category_en].find({}, {'_id': 0})
        if limit:
            query = query.limit(limit)
        products = list(query)
        return products
    return []


def search_products(query):
    """جستجوی محصولات در تمام دسته‌بندی‌ها"""
    db = get_db()
    if db is None:
        return []

    results = []
    categories = [
        "snacks", "spices", "breakfast", "canned_food", "cosmetics",
        "dairy", "drinks", "fruits", "grocery", "home_hygiene",
        "lifestyle", "many", "nuts", "protein_bar", "smokes"
    ]

    for category in categories:
        if category in db.list_collection_names():
            # جستجو در نام محصول
            products = list(db[category].find({
                'name': {'$regex': query, '$options': 'i'}
            }, {'_id': 0}).limit(10))

            for product in products:
                product['category'] = category
                results.append(product)

    return results[:30]  # حداکثر 30 نتیجه