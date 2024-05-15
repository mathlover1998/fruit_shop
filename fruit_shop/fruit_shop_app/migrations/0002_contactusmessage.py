# Generated by Django 5.0 on 2024-05-14 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_shop_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUsMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('subject', models.CharField(max_length=255)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': 'Contact Us Message',
                'verbose_name_plural': 'Contact Us Messages',
                'db_table': 'ContactUsMessages',
                'ordering': ['id'],
                'managed': True,
            },
        ),
    ]