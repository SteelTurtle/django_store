from django.core.urlresolvers import reverse
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

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'year': self.publication_date.year,
                                                   'month': self.publication_date.month,
                                                   'slug': self.slug})

    def __str__(self):
        return '{} published on {}'.format(self.title, self.publication_date.strftime('%d-%m-%Y'))

    class Meta:
        # order blog posts from oldest to newest AND title
        ordering = ['-publication_date', 'title']
        get_latest_by = 'publication_date'
