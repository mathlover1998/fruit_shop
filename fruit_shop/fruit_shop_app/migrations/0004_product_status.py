# Generated by Django 5.0 on 2024-04-11 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_shop_app', '0003_category_parent_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]