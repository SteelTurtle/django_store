from django.shortcuts import get_object_or_404, render

from .models import Product, Tag


def product_detail(request, slug):
    product = get_object_or_404(Product, slug__iexact=slug)
    template = 'product/product_detail.html'
    return render(request, template, {'product': product})


def product_list(request):
    template = 'product/product_list.html'
    return render(request, template, {'product_list': Product.objects.all()})


def tag_list(request):
    template = 'product/tag_list.html'
    return render(request, template, {'tag_list': Tag.objects.all()})


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug__iexact=slug)
    template = 'product/tag_detail.html'
    return render(request, template, {'tag': tag})
