from django import forms
from django.core.exceptions import ValidationError

from .models import Link, Product, Tag


class SlugCleanMixin:
    """Mixin Class for the common "clean_slug" methods in the forms."""

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug cannot be "create". That is a reserved word')
        return new_slug


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = '__all__'


class ProductForm(SlugCleanMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class TagForm(SlugCleanMixin, forms.ModelForm):
    # inherit all the Tag's model fields
    class Meta:
        model = Tag
        fields = '__all__'

    # by convention, because this form is a ModelForm, all the clean methods must start with "clean_"
    def clean_name(self):
        return self.cleaned_data['name'].lower()
