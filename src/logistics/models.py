from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Account(models.Model):
    class Meta:
        db_table = 'logi_account'
        ordering = []

    def __str__(self):
        return ""

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(
        max_length=50, blank=True, null=True)
    user = models.OneToOneField(
        User, blank=True, null=True, help_text="Which user", on_delete=models.PROTECT)
    bank_id = models.CharField(
        max_length=10, blank=True, null=True, help_text="銀行代碼")
    account_id = models.CharField(
        max_length=50, blank=True, null=True, help_text="帳號")
    create_time = models.DateTimeField(auto_now_add=True)


class Storage(models.Model):
    class Meta:
        db_table = 'logi_storage'
        ordering = []

    def __str__(self):
        return ""

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)

    name = models.CharField(
        max_length=20, blank=True, null=True, help_text="倉庫名稱")
    description = models.CharField(
        max_length=200, blank=True, null=True, help_text="說明")
    address = models.CharField(
        max_length=50, blank=True, null=True, help_text="地址")
    owner = models.ForeignKey(
        Account, blank=True, null=True, help_text="倉庫主人", on_delete=models.PROTECT)


class Delivery(models.Model):
    class Meta:
        db_table = 'logi_delivery'
        ordering = []

    def __str__(self):
        return ""

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)

    type = models.CharField(
        max_length=10, blank=True, null=True, help_text="交貨方式")  # 面交/郵寄/店到店/轉交
    location = models.CharField(
        max_length=50, blank=True, null=True, help_text="交貨地點")  # 面交地點/郵寄地址/店到店店名/轉交地點
    time = models.DateTimeField(
        blank=True, null=True, help_text="交貨時間")  # 面交時間/寄出時間/轉交託付時間

    price = models.PositiveIntegerField(
        blank=True, null=True, help_text="交貨金額")
    is_paid = models.BooleanField(
        default=False, help_text="委託人是否已繳錢")

    owner = models.ForeignKey(Account, blank=True, null=True,
                              related_name="delivery_owner", help_text="下單者", on_delete=models.PROTECT)
    proxy = models.ForeignKey(Account, blank=True, null=True,
                              related_name="delivery_proxy", help_text="轉交人", on_delete=models.PROTECT)
    contractor = models.ForeignKey(Account, blank=True, null=True,
                                   related_name="delivery_contractor", help_text="委託人", on_delete=models.PROTECT)


class Order(models.Model):
    class Meta:
        db_table = 'logi_order'
        ordering = ["-create_time"]

    def __str__(self):
        return self.delivery_id

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        Account, blank=True, null=True, help_text="下單者", on_delete=models.PROTECT)
    delivery_cost = models.PositiveIntegerField(
        blank=True, null=True, help_text="運費")
    delivery_id = models.CharField(
        max_length=50, blank=True, null=True, help_text="運輸單號")
    delivery_name = models.CharField(
        max_length=50, blank=True, null=True, help_text="運輸業者")
    delivery_status = models.CharField(
        max_length=10, blank=True, null=True, help_text="運輸狀態")  # 未出貨/已出貨/到達倉庫/已寄出/已交貨
    expect_arrival = models.DateField(
        blank=True, null=True, help_text="預定到貨日期")

    storage = models.ForeignKey(
        Storage, blank=True, null=True, help_text="隸屬倉庫", on_delete=models.PROTECT)

    hint = models.CharField(
        max_length=500, blank=True, null=True, help_text="備註")


class Item(models.Model):
    class Meta:
        db_table = 'logi_item'
        ordering = ["-create_time", "name"]

    def __str__(self):
        return self.name

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)

    name = models.CharField(
        max_length=50, blank=True, null=True, help_text="物品名稱")
    count = models.PositiveIntegerField(
        blank=True, null=True, help_text="數量")

    price = models.PositiveIntegerField(blank=True, null=True, help_text="金額")
    is_paid = models.BooleanField(
        default=False, help_text="委託人是否已繳錢")

    order = models.ForeignKey(
        Order, blank=True, null=True, help_text="隸屬訂單", on_delete=models.PROTECT)

    contractor = models.ForeignKey(Account, blank=True, null=True,
                                   related_name="item_contractor", help_text="委託人", on_delete=models.PROTECT)
    delivery = models.ForeignKey(
        Delivery, blank=True, null=True, help_text="交貨安排", on_delete=models.PROTECT)
