from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import ArchiveIndexView, CreateView, MonthArchiveView, View, YearArchiveView

from .forms import PostForm
from .models import Post


class PostArchiveYear(YearArchiveView):
    model = Post
    date_field = 'publication_date'
    make_object_list = True


class PostArchiveMonth(MonthArchiveView):
    model = Post
    date_field = 'publication_date'
    month_format = '%m'


@require_http_methods(['HEAD', 'GET'])
def post_detail(request, year, month, slug):
    post = get_object_or_404(
        Post,
        publication_date__year=year,
        publication_date__month=month,
        slug=slug)
    return render(
        request,
        'blog/post_detail.html',
        {'post': post})


class PostList(ArchiveIndexView):
    allow_empty = True
    allow_future = True
    context_object_name = 'post_list'
    date_field = 'publication_date'
    make_object_list = True
    model = Post
    paginate_by = 5
    template_name = 'blog/post_list.html'


class PostCreate(CreateView):
    form_class = PostForm
    template_name = 'blog/post_form.html'


class PostDelete(View):
    def get(self, request, year, month, slug):
        post = get_object_or_404(Post,
                                 publication_date__year=year,
                                 publication_date__month=month,
                                 slug__iexact=slug)
        return render(request, 'blog/post_confirm_delete.html', {'post': post})

    def post(self, request, year, month, slug):
        post = get_object_or_404(Post,
                                 publication_date__year=year,
                                 publication_date__month=month,
                                 slug__iexact=slug)
        post.delete()
        return redirect('blog_post_list')


class PostUpdate(View):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_form_update.html'

    def get(self, request, year, month, slug):
        # check if the object we are looking for does exist;
        # if not, get http 404
        post = get_object_or_404(self.model,
                                 publication_date__year=year,
                                 publication_date__month=month,
                                 slug__iexact=slug)
        context = {'form': self.form_class(instance=post),
                   'post': post}
        return render(request, self.template_name, context)

    def post(self, request, year, month, slug):
        # same as GET: before we try to update let's check
        # this object does actually exist
        post = get_object_or_404(self.model,
                                 publication_date__year=year,
                                 publication_date__month=month,
                                 slug__iexact=slug)
        bound_form = self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        else:
            context = {'form': bound_form,
                       'post': post}
            return render(request, self.template_name, context)
