from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    # uniqueness of each post is guaranteed by the publication year + month + its slug
    # So, no need to check specific uniqueness of the slug
    def clean_slug(self):
        return self.cleaned_data['slug'].lower()
