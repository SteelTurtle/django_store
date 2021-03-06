from django.conf.urls import url

from .views import (LinkCreate,
                    LinkDelete,
                    LinkUpdate,
                    ProductCreate,
                    ProductDelete,
                    ProductDetail,
                    ProductList,
                    ProductUpdate,
                    TagCreate,
                    TagDelete,
                    TagDetail,
                    TagList,
                    TagUpdate)

urlpatterns = [
    url(r'^link/create/$', LinkCreate.as_view(), name='product_link_create'),
    url(r'^link/update/(?P<pk>\d+)/$', LinkUpdate.as_view(), name='product_link_update'),
    url(r'^link/delete/(?P<pk>\d+)/$', LinkDelete.as_view(), name='product_link_delete'),
    url(r'^product/$', ProductList.as_view(), name='product_product_list'),
    url(r'^product/create/$', ProductCreate.as_view(), name='product_product_create'),
    url(r'^product/(?P<slug>[\w\-]+)/$', ProductDetail.as_view(), name='product_product_detail'),
    url(r'^product/(?P<slug>[\w\-]+)/delete/$', ProductDelete.as_view(), name='product_product_delete'),
    url(r'^product/(?P<slug>[\w\-]+)/update/$', ProductUpdate.as_view(), name='product_product_update'),
    url(r'^tag/$', TagList.as_view(), name='product_tag_list'),
    # the "tag/create" path must be matched BEFORE the pattern described by tag_detail view
    # otherwise we will always be sent to the wrong page
    url(r'^tag/create/$', TagCreate.as_view(), name='product_tag_create'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', TagDetail.as_view(), name='product_tag_detail'),
    url(r'^tag/(?P<slug>[\w\-]+)/delete/$', TagDelete.as_view(), name='product_tag_delete'),
    url(r'^tag/(?P<slug>[\w\-]+)/update/$', TagUpdate.as_view(), name='product_tag_update'),
]
