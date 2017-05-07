from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import LinkForm, ProductForm, TagForm
from .models import Product, Tag


class LinkCreate(View):
    form_class = LinkForm
    template_name = 'product/product_link_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_link = bound_form.save()
            return redirect(new_link)
        else:
            return render(request, self.template_name, {'form': bound_form})


class ProductCreate(View):
    form_class = ProductForm
    template_name = 'product/product_form.html'

    # GET
    def get(self, request):
        return render(self.template_name, {'form': self.form_class()})

    # POST
    def post(self, request):
        bound_form = self.form_class(request.POST)
        # posted bound_form data are valid
        if bound_form.is_valid():
            new_product = bound_form.save()
            # redirect uses the "get_absolute_url" method of the newly created Product instance
            # to redirect the user to the tag_detail.html page of "new_tag"
            return redirect(new_product)
        # posted bound_form data are invalid
        else:
            return render(request, self.template_name, {'form': bound_form})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug__iexact=slug)
    template = 'product/product_detail.html'
    return render(request, template, {'product': product})


def product_list(request):
    template = 'product/product_list.html'
    return render(request, template, {'product_list': Product.objects.all()})


# A CBV implicitly returns HTTP code 405 if none of the GET or POST request methods are matched
class TagCreate(View):
    form_class = TagForm
    template_name = 'product/tag_form.html'

    # GET
    def get(self, request):
        return render(self.template_name, {'form': self.form_class()})

    # POST
    def post(self, request):
        bound_form = self.form_class(request.POST)
        # posted bound_form data are valid
        if bound_form.is_valid():
            new_tag = bound_form.save()
            # redirect uses the "get_absolute_url" method of the newly created Tag instance
            # to redirect the user to the tag_detail.html page of "new_tag"
            return redirect(new_tag)
        # posted bound_form data are invalid
        else:
            return render(request, self.template_name, {'form': bound_form})


def tag_list(request):
    template = 'product/tag_list.html'
    return render(request, template, {'tag_list': Tag.objects.all()})


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug__iexact=slug)
    template = 'product/tag_detail.html'
    return render(request, template, {'tag': tag})

