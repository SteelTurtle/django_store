from django.conf.urls import url

from blog.views import (PostArchiveMonth,
                        PostArchiveYear,
                        PostCreate,
                        PostDelete,
                        PostList,
                        PostUpdate,
                        post_detail)

urlpatterns = [
    url(r'^$', PostList.as_view(), name='blog_post_list'),
    url(r'^create/$', PostCreate.as_view(), name='blog_post_create'),
    url(r'^(?P<year>\d{4})/$', PostArchiveYear.as_view(), name='blog_post_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', PostArchiveMonth.as_view(), name='blog_post_archive_month'),
    url(r'^(?P<year>\d{4})/'
        r'(?P<month>\d{1,2})/'
        r'(?P<slug>[\w\-]+)/$',
        post_detail, name='blog_post_detail'),
    url(r'^(?P<year>\d{4})/'
        r'(?P<month>\d{1,2})/'
        r'(?P<slug>[\w\-]+)/'
        r'delete/$', PostDelete.as_view(), name='blog_post_delete'),
    url(r'^(?P<year>\d{4})/'
        r'(?P<month>\d{1,2})/'
        r'(?P<slug>[\w\-]+)/'
        r'update/$', PostUpdate.as_view(), name='blog_post_update'),
]
