from django import forms
from django.utils.text import slugify

from .models import Post, Tag


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=True,
                                              widget=forms.TextInput(attrs={'class': 'form-control badge-pill'}))
        self.fields['slug'] = forms.SlugField(required=True,
                                              widget=forms.TextInput(attrs={'class': 'form-control badge-pill'}))

    class Meta:
        model = Tag
        fields = ['name', 'slug']

    def save(self, commit=True):
        self_object = super().save(commit=False)
        self_object.slug = slugify(self.cleaned_data['slug'].strip())
        if commit:
            self_object.save()
        return self_object
