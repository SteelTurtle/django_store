from django.core.urlresolvers import reverse

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=31, db_index=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label identifying the product URL')
    description = models.TextField(blank=True, null=True)
    added_to_catalogue = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category')
    tags = models.ManyToManyField('Tag')

    def get_absolute_url(self):
        return reverse('product_product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        get_latest_by = 'added_to_catalogue'


class Category(models.Model):
    title = models.CharField(max_length=127)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label identifying the category URL')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_absolute_url(self):
        return reverse('product_category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label identifying the tag URL')

    def get_absolute_url(self):
        return reverse('product_tag_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        # defaults ordering tags by name
        ordering = ['name']


class Link(models.Model):
    title = models.CharField(max_length=63)
    publication_date = models.DateField(verbose_name='date published')
    link_url = models.URLField()
    product = models.ForeignKey('Product')

    def __str__(self):
        return '{}:{}'.format(self.product, self.title)

    class Meta:
        # set a verbose name for the class
        verbose_name = 'product link'
        # order by publication date (oldest to newest)
        ordering = ['-publication_date']
        get_latest_by = 'publication_date'
