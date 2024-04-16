from django.contrib import admin
import django.apps
from models import *
from django import forms

#create new admin site instead of the default one
# class FruitShopAdmin(admin.AdminSite):
#     #set header of new admin site
#     site_header = 'Fruit shop admin site'
#config login page for admin site bind with Fruitshop admin site 
#     login_template = 'admin/login.html'  

# fruitshop_site = FruitShopAdmin(name='FruitshopAdmin')

#after that need change in urls.py
# urlpatterns = [
#     path('fruitshopadmin/',fruitshop_site.urls)
# ]


#get all models in project
# models = django.apps.apps.get_models()
# print(models)

#register all models
# for model in models:
#     try:
#         admin.site.regiter(model)
#     #except those models which already registered
#     except admin.sites.AlreadyRegistered:
#         pass

#unregister a model
# admin.site.unregister()

# TEXT = 'Some test text'
# class ProductAdmin(admin.ModelAdmin):
#     #fields can be group
#     fields = ['product_name',('price', 'stock_quantity')]
#     #fields can be section
#     fieldsets = (
#         ('Section 1',{
#             'fields': ('product_name'),
#             #display TEXT
#             'description': '%s' % TEXT,
#         }),
#         ('Section 2',{
#             'fields': ('price','stock_quantity'),
#             #make section display hide/show
#             'classes':('collapse',),
#         })
#     )

#add help_text to field in model to display text

# class ProductForm(forms.ModelForm):
#     def __init__(self,*args, **kwargs):
#         super(ProductForm,self).__init__(*args, **kwargs)
#         self.fields['product_name'].help_text = 'New Help text'
#     class Meta:
#         model = Product
#         exclude = ('',)

# class ProductFormAdmin(admin.ModelAdmin):
#     form = ProductForm

# admin.site.register(Product,ProductFormAdmin)