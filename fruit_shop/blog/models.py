from django.db import models
from django.utils import timezone
from fruit_shop_app.models import User, Category


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255, null=False)

    class Meta:
        ordering = ["id"]
        db_table = "Tags"
        managed = True
        verbose_name = "Tag Table"
        verbose_name_plural = "Tags Table"


class Blog(models.Model):
    title = models.CharField(
        null=False, max_length=100, default="", help_text="Title of blog"
    )
    subtitle = models.CharField(max_length=255, null=False, default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    date = models.DateField(auto_now_add=True)
    content = models.TextField(null=True)
    slug = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name="blogs")
    tags = models.ManyToManyField(Tag, related_name="blogs")

    class Meta:
        ordering = ["id"]
        db_table = "Blogs"
        managed = True
        verbose_name = "Blog Table"
        verbose_name_plural = "Blogs Table"


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to="images/blog_images/", default="images/default/default_blog.png"
    )

    class Meta:
        ordering = ["id"]
        db_table = "BlogImages"
        managed = True
        verbose_name = "Blog Image Table"
        verbose_name_plural = "Blog Images Table"
