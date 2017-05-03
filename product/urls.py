from django.conf.urls import url

from .views import product_detail, product_list, tag_detail, tag_list

urlpatterns = [
    url(r'^product$', product_list, name='product_product_list'),
    url(r'^product/(?P<slug>[\w\-]+)$', product_detail, name='product_product_detail'),
    url(r'^tag/$', tag_list, name='product_tag_list'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', tag_detail, name='product_tag_detail'),

]
