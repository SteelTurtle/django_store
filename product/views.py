from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DeleteView, UpdateView, View

from .forms import LinkForm, ProductForm, TagForm
from .models import Link, Product, Tag


class LinkCreate(CreateView):
    form_class = LinkForm
    template_name = 'product/link_form.html'


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


class LinkDelete(DeleteView):
    # The get_success_url() method is called before the NewsLink instance is deleted
    # from the database
    def get_success_url(self):
        return self.object.product.get_absolute_url()


class ProductCreate(CreateView):
    form_class = ProductForm
    template_name = 'product/product_form.html'


def product_detail(request, slug):
    product = get_object_or_404(Product, slug__iexact=slug)
    template = 'product/product_detail.html'
    return render(request, template, {'product': product})


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('product_product_list')


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
        else:
            next_url = None

        # let's inject additional paginator data to the context,
        # so we can have less calls on the template
        context = {'product_list': page,
                   'paginator': paginator,
                   'is_paginated': page.has_other_pages(),
                   'next_page_url': next_url,
                   'previous_page_url': previous_url,
                   }
        return render(request, self.template_name, context)


class ProductUpdate(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product/product_form_update.html'


# A CBV implicitly returns HTTP code 405 if none of the GET or POST request methods are matched
class TagCreate(CreateView):
    form_class = TagForm
    template_name = 'product/tag_form.html'


class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('product_tag_list')


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug__iexact=slug)
    template = 'product/tag_detail.html'
    return render(request, template, {'tag': tag})


def tag_list(request):
    template = 'product/tag_list.html'
    return render(request, template, {'tag_list': Tag.objects.all()})


class TagUpdate(UpdateView):
    form_class = TagForm
    model = Tag
    template_name = 'product/tag_form_update.html'
