from django.http.response import HttpResponse
from django.template import loader

from .models import Tag


def homepage(request):
    tag_list = Tag.objects.all()
    template = loader.get_template('product/tag_list.html')
    output = template.render({'tag_list': tag_list})
    return HttpResponse(output)


def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    template = loader.get_template('product/tag_detail.html')
    output = template.render({'tag': tag})
    return HttpResponse(output)
