from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import LinkForm, ProductForm, TagForm
from .models import Link, Product, Tag
from .utils import PageLinksMixin


class LinkCreate(CreateView):
    form_class = LinkForm
    template_name = 'product/link_form.html'


class LinkUpdate(UpdateView):
    form_class = LinkForm
    model = Link
    template_name_suffix = '_form_update'


class LinkDelete(DeleteView):
    # The get_success_url() method is called before the NewsLink instance is deleted
    # from the database.
    # In StartupDelete and TagDelete , we were able to set the success url attribute
    # using reverse_lazy() because we simply wanted to redirect to a list page. When deleting
    # Link objects, we want to redirect to the page the user was just on: the detail page of
    # the Startup that the Link was associated with. This page cannot be set by an
    # attribute because it changes from instance to instance. Instead, we can override the
    # get_success_url() method,
    def get_success_url(self):
        return self.object.product.get_absolute_url()


class ProductCreate(CreateView):
    form_class = ProductForm
    template_name = 'product/product_form.html'


class ProductDetail(DetailView):
    model = Product


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('product_product_list')


class ProductList(PageLinksMixin, ListView):
    model = Product
    paginate_by = 5


class ProductUpdate(UpdateView):
    form_class = ProductForm
    model = Product
    template_name_suffix = '_form_update'


# A CBV implicitly returns HTTP code 405 if none of the GET or POST request methods are matched
class TagCreate(CreateView):
    form_class = TagForm
    template_name = 'product/tag_form.html'


class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('product_tag_list')


class TagDetail(DetailView):
    model = Tag


class TagList(PageLinksMixin, ListView):
    paginate_by = 5
    model = Tag


class TagUpdate(UpdateView):
    form_class = TagForm
    model = Tag
    template_name_suffix = '_form_update'
