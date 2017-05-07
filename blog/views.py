from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import PostForm
from .models import Post


def post_detail(request, year, month, slug):
    post = get_object_or_404(Post.objects
                             .filter(publication_date__year=year)
                             .filter(publication_date__month=month)
                             .get(slug__iexact=slug))
    return render(request, 'blog/post_detail.html', {'post': post})


class PostList(View):
    def get(self, request):
        return render(request, 'blog/post_list.html', {'post_list': Post.objects.all()})


class PostCreate(View):
    form_class = PostForm
    template_name = 'blog/post_form.html'

    # GET
    def get(self, request):
        return render(self.template_name, {'form': self.form_class()})

    # POST
    def post(self, request):
        bound_form = self.form_class(request.POST)
        # posted bound_form data are valid
        if bound_form.is_valid():
            new_post = bound_form.save()
            # redirect uses the "get_absolute_url" method of the newly created Post instance
            # to redirect the user to the post_detail.html page of "new_post"
            return redirect(new_post)
        # posted bound_form data are invalid
        else:
            return render(request, self.template_name, {'form': bound_form})
