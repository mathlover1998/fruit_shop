# Generated by Django 5.0 on 2024-04-24 11:46

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_shop_app', '0003_rename_discount_code_discount_code_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'managed': True, 'ordering': ['-placed_at'], 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_status',
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_orders', to='fruit_shop_app.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('momo', 'Momo')], default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_transaction',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='placed_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_orders', to='fruit_shop_app.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('complete', 'Complete'), ('refunded', 'Refunded'), ('failed', 'Failed'), ('shipped', 'Shipped'), ('cancelled', 'Cancelled')], default='pending'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('momo', 'Momo')], default='cash'),
        ),
    ]
