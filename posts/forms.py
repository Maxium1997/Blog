from datetime import datetime
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


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(PostForm, self).__init__(*args, **kwargs)
    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'border-0 p-2 h1 font-weight-light',
                                                          'placeholder': 'Title',
                                                          'autofocus': 'autofocus'}))
    content = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows': '12',
                                                           'class': 'border-0 p-2 h5 font-weight-light',
                                                           'placeholder': 'What do you think?'}))

    def save(self, commit=True):
        post = super().save(commit=False)
        post.author = self.author
        post.updated_time = datetime.now()
        if commit:
            post.save()
        return post

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
