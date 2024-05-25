from celery import shared_task
import pandas as pd
from fruit_shop_app.models import Product, Category, Brand, ProductImage
from common.utils import handle_uploaded_file, convert_to_csv, crop_image, upload_file_to_s3
from django.conf import settings
import os
from io import BytesIO
from uuid import uuid4

@shared_task
def process_upload(file_path, user_id):
    csv_file_path = convert_to_csv(file_path)
    try:
        df = pd.read_csv(csv_file_path)
        if df.empty:
            return {'error': 'The uploaded file is empty or invalid'}

        for index, row in df.iterrows():
            categories = Category.objects.filter(category_name=row.iloc[9])
            brand = Brand.objects.filter(brand_name=row.iloc[8]).first()
            common_args = {
                "brand": brand,
                "product_name": row.iloc[0],
                "price": row.iloc[1],
                "stock_quantity": row.iloc[4],
                "origin_country": row.iloc[5],
                "information": row.iloc[6],
                "unit": row.iloc[3],
                "inventory_manager_id": user_id
            }
            if not pd.isna(row.iloc[7]):
                common_args["sku"] = row.iloc[7]

            product = Product.objects.create(**common_args)
            product.save()
            all_categories = set(categories)
            for category in categories:
                current_category = category
                while current_category.parent_category:
                    all_categories.add(current_category.parent_category)
                    current_category = current_category.parent_category
            product.categories.set(all_categories)

            local_file_path = row.iloc[2]
            cropped_image = crop_image(local_file_path)
            image_name = f"images/product_images/{uuid4().hex}.jpg"
            in_memory_file = BytesIO()
            cropped_image.save(in_memory_file, format='JPEG')
            in_memory_file.seek(0)
            upload_file_to_s3(data=in_memory_file, bucket=settings.AWS_STORAGE_BUCKET_NAME, object_name=image_name)
            ProductImage.objects.create(product=product, image=image_name).save()
            print('Done')

        return {'status': 'success'}
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)