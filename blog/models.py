from django.db import models

from product.models import Product, Tag


class Post(models.Model):
    title = models.CharField(max_length=63)
    slug = models.SlugField(max_length=63,
                            unique_for_month='publication_date',
                            help_text='A label identifying the blog post URL')
    text = models.TextField()
    publication_date = models.DateField(verbose_name='date published', auto_now_add=True)
    products = models.ManyToManyField(Product)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
