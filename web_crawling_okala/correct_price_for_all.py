from db_config import get_collection

collection = get_collection("many") # ....



# پیدا کردن محصولاتی که قیمتشون "تومان" نداره
products = collection.find({"price": {"$not": {"$regex": "تومان"}}})

count = 0
for product in products:
    old_price = product["price"]

    # فقط اگه قیمت "ناموجود" نباشه
    if old_price != "ناموجود":
        new_price = f"{old_price} تومان"
        collection.update_one(
            {"_id": product["_id"]},
            {"$set": {"price": new_price}}
        )
        print(f"✅ {product['name'][:35]} -> {new_price}")
        count += 1

print(f"\n🎯 {count} محصول اصلاح شد.")