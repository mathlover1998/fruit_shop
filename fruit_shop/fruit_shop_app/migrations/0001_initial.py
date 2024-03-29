# Generated by Django 5.0 on 2024-03-28 12:50

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('description', models.TextField(default='')),
            ],
            options={
                'verbose_name': 'Category Table',
                'verbose_name_plural': 'Categories Table',
                'db_table': 'Categories',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_code', models.CharField(max_length=20)),
                ('discount_percentage', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('valid_from', models.DateField()),
                ('valid_to', models.DateField()),
                ('min_purchase_amount', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Discount Table',
                'verbose_name_plural': 'Discounts Table',
                'db_table': 'Discounts',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(max_length=100)),
                ('contact_person', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(help_text='Enter your phone number', max_length=15)),
            ],
            options={
                'verbose_name': 'Supplier Table',
                'verbose_name_plural': 'Suppliers Table',
                'db_table': 'Suppliers',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=20, null=True)),
                ('middle_name', models.CharField(blank=True, default='', max_length=255)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other', max_length=20)),
                ('dob', models.DateField(default='2000-01-01')),
                ('image', models.ImageField(default='images/default-avatar.png', upload_to='images/')),
                ('receive_updates', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User Table',
                'verbose_name_plural': 'Users Table',
                'db_table': 'Users',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ConfirmationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Confirmation Token Table',
                'verbose_name_plural': 'Confirmation Tokens Table',
                'db_table': 'ConfirmationTokens',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Table',
                'verbose_name_plural': 'Customers Table',
                'db_table': 'Customers',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hire_date', models.DateField(null=True)),
                ('salary', models.IntegerField(default=0)),
                ('department', models.CharField(default='', max_length=200)),
                ('position', models.CharField(choices=[('employee', 'Employee'), ('inventory_manager', 'Inventory Manager'), ('sales_associate', 'Sales Associate'), ('cashier', 'Cashier'), ('store_manager', 'Store Manager'), ('assistant_manager', 'Assistant Manager'), ('delivery_driver', 'Delivery Driver'), ('produce_specialist', 'Produce Specialist'), ('customer_service_representative', 'Customer Service Representative')], default='employee', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employee Table',
                'verbose_name_plural': 'Employees Table',
                'db_table': 'Employees',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_name', models.CharField(max_length=100, null=True)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('street', models.CharField(default='', max_length=255)),
                ('commune', models.CharField(default='', max_length=50, null=True)),
                ('ward', models.CharField(default='', max_length=50, null=True)),
                ('district', models.CharField(default='', max_length=50, null=True)),
                ('province', models.CharField(default='', max_length=50, null=True)),
                ('country', models.CharField(default='', max_length=50)),
                ('zipcode', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('home', 'Home'), ('office', 'Office')], default='home')),
                ('default_address', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.customer')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.employee')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.supplier')),
            ],
            options={
                'verbose_name': 'Address Table',
                'verbose_name_plural': 'Addresses Table',
                'db_table': 'Addresses',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(auto_now=True)),
                ('total_amount', models.IntegerField(default=0)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('complete', 'Complete'), ('refunded', 'Refunded'), ('failed', 'Failed'), ('abandoned', 'Abandoned'), ('on_hold', 'On Hold'), ('cancelled', 'Cancelled')])),
                ('delivery_address', models.CharField(default='', max_length=255)),
                ('delivery_date', models.DateField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.customer')),
            ],
            options={
                'verbose_name': 'Order Table',
                'verbose_name_plural': 'Orders Table',
                'db_table': 'Orders',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_image', models.ImageField(default='images/default_fruit.jpg', upload_to='images/')),
                ('price', models.IntegerField(default=0)),
                ('stock_quantity', models.IntegerField(default=0)),
                ('origin_country', models.CharField(default='', max_length=40)),
                ('information', models.TextField(null=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('expiry_date', models.DateField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.category')),
                ('inventory_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_product', to='fruit_shop_app.employee')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.supplier')),
            ],
            options={
                'verbose_name': 'Product Table',
                'verbose_name_plural': 'Products Table',
                'db_table': 'Products',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('subtotal', models.IntegerField(default=0)),
                ('discount_applied', models.CharField(default='', max_length=30)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.product')),
            ],
            options={
                'verbose_name': 'Order Item Table',
                'verbose_name_plural': 'Order Items Table',
                'db_table': 'OrderItems',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StoreLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(default='', max_length=50)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.address')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.employee')),
            ],
            options={
                'verbose_name': 'Store Location Table',
                'verbose_name_plural': 'Store Locations Table',
                'db_table': 'StoreLocations',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField(auto_now=True)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('momo', 'Momo'), ('apple_pay', 'Apple Pay'), ('mobile_banking', 'Mobile Banking')])),
                ('amount_paid', models.FloatField(default=0.0)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.order')),
            ],
            options={
                'verbose_name': 'Transaction Table',
                'verbose_name_plural': 'Transactions Table',
                'db_table': 'Transactions',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['first_name', 'middle_name', 'last_name'], name='full_name'),
        ),
    ]
