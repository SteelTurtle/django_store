from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import LinkForm, ProductForm, TagForm
from .models import Link, Product, Tag


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


class LinkUpdate(View):
    form_class = LinkForm
    template_name = 'product/link_form_update.html'

    def get(self, request, pk):
        link = get_object_or_404(Link, pk=pk)
        context = {'form': self.form_class(instance=link),
                   'link': link}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        link = get_object_or_404(Link, pk=pk)
        bound_form = self.form_class(request.POST, instance=link)
        if bound_form.is_valid():
            new_link = bound_form.save()
            return redirect(new_link)
        else:
            context = {'form': bound_form,
                       'link': link}
            return render(request, self.template_name, context)


class LinkDelete(View):
    pass


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


class ProductDelete(View):
    pass


class ProductList(View):
    page_kwargs = 'page'
    objects_per_page = 5
    template_name = 'product/product_list.html'

    def get(self, request):
        product_list = Product.objects.all()
        # let's paginate the list!
        paginator = Paginator(product_list, self.objects_per_page)
        # check which page to move to next:
        # extract the value of 'page' from the current http request context
        # resulted from a GET request, and pass the obtained page number to the caller
        page_number = request.GET.get(self.page_kwargs)
        # of course we need to account for situations like empty or
        # non conventional 'page' values passed by the user
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        # Also, we account for situations where the '?page=something' is not specified in the url
        if page.has_previous():
            previous_url = '?{pkw}={n}'.format(pkw=self.page_kwargs, n=page.previous_page_number())
        else:
            previous_url = None
        if page.has_next():
            next_url = '?{pkw}={n}'.format(pkw=self.page_kwargs, n=page.next_page_number())

        # let's inject additional paginator data to the context,
        # so we can have less calls on the template
        context = {'is_paginated': page.has_other_pages(),
                   'next_page_url': next_url,
                   'paginator': paginator,
                   'previous_page_url': previous_url,
                   'product_list': page}
        return render(request, self.template_name, context)


class ProductUpdate(View):
    pass


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


class TagDelete(View):
    pass


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug__iexact=slug)
    template = 'product/tag_detail.html'
    return render(request, template, {'tag': tag})


def tag_list(request):
    template = 'product/tag_list.html'
    return render(request, template, {'tag_list': Tag.objects.all()})


class TagUpdate(View):
    pass
