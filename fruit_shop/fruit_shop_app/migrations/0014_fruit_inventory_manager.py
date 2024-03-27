# Generated by Django 5.0 on 2024-03-27 21:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_shop_app', '0013_alter_employee_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruit',
            name='inventory_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_fruits', to='fruit_shop_app.employee'),
        ),
    ]
