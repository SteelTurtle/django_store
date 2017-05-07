from django.conf.urls import url

from .views import LinkCreate, ProductCreate, TagCreate, product_detail, product_list, tag_detail, tag_list

urlpatterns = [
    url(r'^link/create/$', LinkCreate.as_view(), name='product_link_create'),
    url(r'^product$', product_list, name='product_product_list'),
    url(r'^product/create/$', ProductCreate.as_view(), name='product_product_create'),
    url(r'^product/(?P<slug>[\w\-]+)$', product_detail, name='product_product_detail'),
    url(r'^tag/$', tag_list, name='product_tag_list'),
    # the "tag/create" path must be matched BEFORE the pattern described by tag_detail view
    # otherwise we will always be sent to the wrong page
    url(r'^tag/create/$', TagCreate.as_view(), name='product_tag_create'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', tag_detail, name='product_tag_detail'),

]
