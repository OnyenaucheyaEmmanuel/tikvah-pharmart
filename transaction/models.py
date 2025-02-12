# from itertools import product
from django.db import models
from django.conf import settings
from django.db.models import F
from inventory.models import product, PERCENTAGE_VALIDATOR
import pytz
timezone = pytz.timezone("US/Eastern")

from django.db import models
from django.conf import settings
from django.db.models import F
from inventory.models import product, PERCENTAGE_VALIDATOR
import pytz
from django.contrib.auth.models import User
from decimal import Decimal

timezone = pytz.timezone("US/Eastern")

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bonus_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def earn_bonus(self, amount_spent):
        """For every ₦20,000 spent, the customer gets ₦500 bonus"""
        self.total_spent += Decimal(amount_spent)
        new_bonus = (Decimal(amount_spent) // 20000) * 500
        self.bonus_balance += new_bonus
        self.save()

    def redeem_bonus(self, amount):
        """Redeem up to the available bonus balance"""
        if amount <= self.bonus_balance:
            self.bonus_balance -= amount
            self.save()
            return amount
        return Decimal(0)

    def __str__(self):
        return f"{self.name} - Bonus: ₦{self.bonus_balance}"

# from itertools import product
from django.db import models
from django.conf import settings
from django.db.models import F
from inventory.models import product, PERCENTAGE_VALIDATOR
import pytz
timezone = pytz.timezone("US/Eastern")


# Create your models here.transaction_dt
class transaction(models.Model):
    date_time       = models.DateTimeField(auto_now_add=True)
    transaction_dt  = models.DateTimeField(editable=False, null=False, blank=False,)
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=False, blank=False,editable=False,)
    transaction_id  = models.CharField(unique=True, max_length=50, editable=False,null=False)
    total_sale      = models.DecimalField(max_digits=7,decimal_places=2,null=False,editable=False)
    sub_total       = models.DecimalField(max_digits=7,decimal_places=2,null=False,editable=False)
    tax_total       = models.DecimalField(max_digits=7,decimal_places=2,null=True,editable=False)
    deposit_total   = models.DecimalField(max_digits=7,decimal_places=2,null=True,editable=False)
    payment_type    = models.CharField(choices=[('CASH','CASH'),('DEBIT/CREDIT','DEBIT/CREDIT'),('EBT','EBT')],max_length=32, null=False,editable=False)
    receipt         = models.TextField(blank=False,null=False,editable=False)
    products        = models.TextField(blank=False,null=False,editable=False)

    def __str__(self) -> str:
        return self.transaction_id

    def save(self,*args,**kwargs):
        self.transaction_dt = timezone.localize(self.transaction_dt)
        super().save(*args, **kwargs)
        for product_item in eval(self.products):
            try: item = product.objects.get(barcode = product_item['barcode'])
            except: item = product.objects.get(barcode = product_item['barcode'].split("_")[0])
            productTransaction.objects.create(transaction = self, transaction_id_num = self.transaction_id, transaction_date_time = self.transaction_dt,
                                              barcode = product_item['barcode'], name = product_item['name'], department = item.department.department_name, sales_price= product_item['price'],
                                              qty = product_item['quantity'], cost_price = item.cost_price, tax_category = item.tax_category.tax_category, tax_percentage= item.tax_category.tax_percentage,
                                              tax_amount = product_item['tax_value'], deposit_category = item.deposit_category.deposit_category, deposit = item.deposit_category.deposit_value,
                                              deposit_amount = product_item['deposit_value'], payment_type= self.payment_type)
        return self

    class Meta:
        verbose_name_plural = "Transactions"


class productTransaction(models.Model):
    transaction             = models.ForeignKey("transaction", on_delete=models.RESTRICT, null=False, blank=False,editable=False,)
    transaction_id_num      = models.CharField(max_length=50, editable=False,null=False)
    transaction_date_time   = models.DateTimeField(editable=False, null=False, blank=False,)
    barcode                 = models.CharField(max_length=32, editable=False, blank = False, null=False)
    name                    = models.CharField(max_length=125, editable=False, blank = False, null = False)
    department              = models.CharField(max_length=125, editable=False,blank = False, null = True)
    sales_price             = models.DecimalField(max_digits=7, editable=False,decimal_places=2,null=False,blank = False)
    qty                     = models.IntegerField(default=0, editable=False, null=True)
    cost_price              = models.DecimalField(max_digits=7,decimal_places=2,editable=False, default=0,null=True)
    tax_category            = models.CharField(max_length=125, editable=False,blank = False, null = False)
    tax_percentage          = models.DecimalField(max_digits=6, decimal_places=3, validators=PERCENTAGE_VALIDATOR,null=False,blank=False)
    tax_amount              = models.DecimalField(max_digits=7,decimal_places=2,editable=False, default=0,null=True)
    deposit_category        = models.CharField(max_length=125, editable=False, blank = False, null = False)
    deposit                 = models.DecimalField(max_digits=7,decimal_places=2,null=False,blank=False)
    deposit_amount          = models.DecimalField(max_digits=7,decimal_places=2,editable=False, default=0,null=True)
    payment_type            = models.CharField(max_length=32, null=False,editable=False)

    def save(self,*args,**kwargs):
        if product.objects.filter(barcode=self.barcode).exists():
            product.objects.filter(barcode=self.barcode).update(qty= F('qty')-self.qty)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.transaction_id_num + "_"+ self.barcode

    class Meta:
        verbose_name_plural = "Product Transactions"

from django.db import models
from django.conf import settings
from django.utils.timezone import now  # Ensure this is imported
from django.db.models import Sum, F

class DailyProfit(models.Model):
    date = models.DateField(default=now)  # Stores the date of the sales
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("date", "user")
        verbose_name_plural = "Daily Profits"

    @property
    def total_profit(self):
        """
        Dynamically calculates total profit for this user on the given date.
        Profit = (Sales Price - Cost Price) * Quantity Sold
        """
        total = productTransaction.objects.filter(
            transaction__user=self.user,
            transaction_date_time__date=self.date
        ).aggregate(
            total_profit=Sum((F('sales_price') - F('cost_price')) * F('qty'))
        )['total_profit'] or 0

        return round(total, 2)  # Ensure profit is rounded to 2 decimal places

    @property
    def total_sales(self):
        """
        Dynamically calculates total sales for this user on the given date.
        Sales = Sales Price * Quantity Sold
        """
        total = productTransaction.objects.filter(
            transaction__user=self.user,
            transaction_date_time__date=self.date
        ).aggregate(
            total_sales=Sum(F('sales_price') * F('qty'))
        )['total_sales'] or 0

        return round(total, 2)

    def __str__(self):
        return f"{self.user.username} - {self.date} - Sales: ₦{self.total_sales} - Profit: ₦{self.total_profit}"


