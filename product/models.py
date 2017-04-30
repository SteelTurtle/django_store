from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=31, db_index=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label identifying the product URL')
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField('Category')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=127)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label identifying the category URL')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label identifying the tag URL')

    def __str__(self):
        return self.name


class Link(models.Model):
    title = models.CharField(max_length=63)
    publication_date = models.DateField(verbose_name='date published')
    link_url = models.URLField()
    product = models.ForeignKey('Product')

    def __str__(self):
        return self.title
