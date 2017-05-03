from django.shortcuts import get_object_or_404, render
from django.views import View

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
