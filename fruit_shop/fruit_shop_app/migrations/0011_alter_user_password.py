# Generated by Django 5.0 on 2024-03-27 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_shop_app', '0010_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='@124Baksa31', max_length=128, verbose_name='password'),
        ),
    ]
