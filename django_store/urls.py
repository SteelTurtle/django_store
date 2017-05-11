"""django_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

from account import urls as account_urls
from blog import urls as blog_urls
from contact import urls as contact_urls
from product import urls as product_urls

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='blog_post_list')),
    url(r'^about/$', TemplateView.as_view(template_name='global/about.html'), name='about_site'),
    url(r'^account/', include(account_urls, app_name='account', namespace='dj-auth')),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include(blog_urls)),
    url(r'^contact/', include(contact_urls)),
    url(r'^', include(product_urls)),
]
