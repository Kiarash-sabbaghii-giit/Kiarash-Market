from django.db import models
from django.utils import timezone
import re


class UserInfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    home_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    plaque = models.CharField(max_length=20, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    national_code = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_image = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class VerificationCode(models.Model):
    email = models.CharField(max_length=100)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def is_valid(self):
        delta = timezone.now() - self.created_at
        return delta.seconds < 300 and not self.is_used

    def __str__(self):
        return f"{self.email} - {self.code}"


class Cart(models.Model):
    user_id = models.IntegerField()
    product_name = models.CharField(max_length=500)
    product_price = models.CharField(max_length=100)
    product_image = models.CharField(max_length=500)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user_id', 'product_name']

    def _extract_number(self, price_str):
        """تبدیل قیمت از رشته به عدد - متد داخلی"""
        if not price_str:
            return 0
        price_str = str(price_str)
        # حذف کاما، تومان، فاصله و کاراکترهای اضافی
        price_str = price_str.replace(',', '').replace('تومان', '').replace(' ', '').strip()
        # استخراج اعداد با regex
        numbers = re.findall(r'\d+', price_str)
        if numbers:
            full_number = ''.join(numbers)
            try:
                return int(full_number)
            except:
                return 0
        return 0

    def get_price_int(self):
        """قیمت واحد محصول به صورت عدد"""
        return self._extract_number(self.product_price)

    def get_total_int(self):
        """قیمت کل این آیتم (قیمت × تعداد) به صورت عدد"""
        return self.get_price_int() * self.quantity

    def get_total(self):
        """قیمت کل این آیتم به صورت رشته فرمت شده"""
        total = self.get_total_int()
        return f"{total:,} تومان" if total > 0 else "۰ تومان"

    def __str__(self):
        return f"{self.product_name} - {self.quantity} عدد"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    ]

    user_id = models.IntegerField()
    user_name = models.CharField(max_length=200)
    user_phone = models.CharField(max_length=15)
    user_email = models.CharField(max_length=200, blank=True, null=True)
    user_address = models.TextField()

    total_amount = models.CharField(max_length=100)  # کل مبلغ به صورت متن
    total_amount_int = models.BigIntegerField(default=0)  # کل مبلغ به صورت عدد

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"سفارش #{self.id} - {self.user_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=500)
    product_price = models.CharField(max_length=100)
    product_image = models.CharField(max_length=500)
    quantity = models.IntegerField()

    def _extract_number(self, price_str):
        """تبدیل قیمت از رشته به عدد - متد داخلی"""
        if not price_str:
            return 0
        price_str = str(price_str)
        price_str = price_str.replace(',', '').replace('تومان', '').replace(' ', '').strip()
        numbers = re.findall(r'\d+', price_str)
        if numbers:
            full_number = ''.join(numbers)
            try:
                return int(full_number)
            except:
                return 0
        return 0

    def get_price_int(self):
        """قیمت واحد محصول به صورت عدد"""
        return self._extract_number(self.product_price)

    def get_total_int(self):
        """قیمت کل این آیتم (قیمت × تعداد) به صورت عدد"""
        return self.get_price_int() * self.quantity

    def get_total(self):
        """قیمت کل این آیتم به صورت رشته فرمت شده"""
        total = self.get_total_int()
        return f"{total:,} تومان" if total > 0 else "۰ تومان"

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


class Category(models.Model):
    category_fa = models.CharField(max_length=200)
    category_en = models.CharField(max_length=100, unique=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.category_fa
