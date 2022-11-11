# Generated by Django 3.2 on 2022-11-11 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_id', models.CharField(blank=True, help_text='銀行代碼', max_length=10, null=True)),
                ('account_id', models.CharField(blank=True, help_text='帳號', max_length=50, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, help_text='Which user', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'logi_account',
                'ordering': [],
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(blank=True, help_text='交貨方式', max_length=10, null=True)),
                ('location', models.CharField(blank=True, help_text='交貨地點', max_length=50, null=True)),
                ('time', models.DateTimeField(blank=True, help_text='交貨時間', null=True)),
                ('price', models.PositiveIntegerField(blank=True, help_text='交貨金額', null=True)),
                ('is_paid', models.BooleanField(default=False, help_text='委託人是否已繳錢')),
                ('contractor', models.ForeignKey(blank=True, help_text='委託人', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='delivery_contractor', to='logistics.account')),
                ('owner', models.ForeignKey(blank=True, help_text='下單者', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='delivery_owner', to='logistics.account')),
                ('proxy', models.ForeignKey(blank=True, help_text='轉交人', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='delivery_proxy', to='logistics.account')),
            ],
            options={
                'db_table': 'logi_delivery',
                'ordering': [],
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, help_text='倉庫名稱', max_length=20, null=True)),
                ('description', models.CharField(blank=True, help_text='說明', max_length=200, null=True)),
                ('address', models.CharField(blank=True, help_text='地址', max_length=50, null=True)),
                ('owner', models.ForeignKey(blank=True, help_text='倉庫主人', null=True, on_delete=django.db.models.deletion.PROTECT, to='logistics.account')),
            ],
            options={
                'db_table': 'logi_storage',
                'ordering': [],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
                ('delivery_cost', models.PositiveIntegerField(blank=True, help_text='運費', null=True)),
                ('delivery_id', models.CharField(blank=True, help_text='運輸單號', max_length=50, null=True)),
                ('delivery_name', models.CharField(blank=True, help_text='運輸業者', max_length=50, null=True)),
                ('delivery_status', models.CharField(blank=True, help_text='運輸狀態', max_length=10, null=True)),
                ('expect_arrival', models.DateField(blank=True, help_text='預定到貨日期', null=True)),
                ('hint', models.CharField(blank=True, help_text='備註', max_length=500, null=True)),
                ('owner', models.ForeignKey(blank=True, help_text='下單者', null=True, on_delete=django.db.models.deletion.PROTECT, to='logistics.account')),
                ('storage', models.ForeignKey(blank=True, help_text='隸屬倉庫', null=True, on_delete=django.db.models.deletion.PROTECT, to='logistics.storage')),
            ],
            options={
                'db_table': 'logi_order',
                'ordering': [],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('mod_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, help_text='物品名稱', max_length=50, null=True)),
                ('count', models.PositiveIntegerField(blank=True, help_text='數量', null=True)),
                ('price', models.PositiveIntegerField(blank=True, help_text='金額', null=True)),
                ('is_paid', models.BooleanField(default=False, help_text='委託人是否已繳錢')),
                ('contractor', models.ForeignKey(blank=True, help_text='委託人', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='item_contractor', to='logistics.account')),
                ('delivery', models.ForeignKey(blank=True, help_text='交貨安排', null=True, on_delete=django.db.models.deletion.PROTECT, to='logistics.delivery')),
                ('order', models.ForeignKey(blank=True, help_text='隸屬訂單', null=True, on_delete=django.db.models.deletion.PROTECT, to='logistics.order')),
            ],
            options={
                'db_table': 'logi_item',
                'ordering': [],
            },
        ),
    ]