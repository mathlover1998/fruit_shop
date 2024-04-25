# Generated by Django 5.0 on 2024-04-25 10:29

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
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100)),
                ('contact_person', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(help_text='Enter your phone number', max_length=15)),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
                'db_table': 'Brands',
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
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other', max_length=20)),
                ('dob', models.DateField(default='2000-01-01')),
                ('image', models.ImageField(default='images/default/default_avatar.png', upload_to='images/user_images/')),
                ('receive_updates', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('approval_email_sent', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='user_memberships', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'Users',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('street_address', models.CharField(max_length=255)),
                ('locality', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('home', 'Home'), ('office', 'Office')], default='home', max_length=50)),
                ('is_default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.brand')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
                'db_table': 'Addresses',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('description', models.TextField(default='')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='fruit_shop_app.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'Categories',
                'ordering': ['id'],
                'managed': True,
            },
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
                'verbose_name': 'Confirmation Token',
                'verbose_name_plural': 'Confirmation Tokens',
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
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'db_table': 'Customers',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, null=True)),
                ('description', models.TextField(blank=True)),
                ('discount_type', models.CharField(choices=[('percentage', 'Percentage'), ('fixed_amount', 'Fixed Amount')], default='percentage')),
                ('discount_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('applies_to', models.CharField(choices=[('all_products', 'All Products'), ('category', 'Category'), ('specific_products', 'Specific Products')], default='all_products', max_length=20)),
                ('valid_from', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_to', models.DateTimeField(blank=True, null=True)),
                ('minimum_purchase', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fruit_shop_app.category')),
            ],
            options={
                'verbose_name': 'Discount',
                'verbose_name_plural': 'Discounts',
                'db_table': 'Discounts',
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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'db_table': 'Employees',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('complete', 'Complete'), ('refunded', 'Refunded'), ('failed', 'Failed'), ('shipped', 'Shipped'), ('cancelled', 'Cancelled')], default='pending')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('momo', 'Momo')], default='', max_length=50)),
                ('payment_transaction', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_orders', to='fruit_shop_app.address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.customer')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_orders', to='fruit_shop_app.address')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'Orders',
                'ordering': ['-placed_at'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('price', models.IntegerField(default=0)),
                ('stock_quantity', models.IntegerField(default=0)),
                ('origin_country', models.CharField(default='', max_length=40)),
                ('information', models.TextField(null=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('expiry_date', models.DateField(null=True)),
                ('sku', models.CharField(default='', max_length=10, unique=True)),
                ('unit', models.CharField(choices=[('kg', 'Kilogram'), ('gr', 'Gram'), ('set', 'Set'), ('pack', 'Pack'), ('unit', 'Unit')], default='unit')),
                ('is_active', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.brand')),
                ('categories', models.ManyToManyField(related_name='products', to='fruit_shop_app.category')),
                ('inventory_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_product', to='fruit_shop_app.employee')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
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
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
                'db_table': 'OrderItems',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='images/default/default_fruit.jpg', upload_to='images/product_images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='fruit_shop_app.product')),
            ],
            options={
                'verbose_name': 'ProductImage',
                'verbose_name_plural': 'ProductImages',
                'db_table': 'ProductImages',
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
                'verbose_name': 'Store Location',
                'verbose_name_plural': 'Store Locations',
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
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('momo', 'Momo')], default='cash')),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fruit_shop_app.order')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'db_table': 'Transactions',
                'ordering': ['id'],
                'managed': True,
            },
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['first_name', 'last_name'], name='full_name'),
        ),
        migrations.AddConstraint(
            model_name='address',
            constraint=models.UniqueConstraint(fields=('user', 'is_default'), name='unique_default_address_per_user'),
        ),
    ]
