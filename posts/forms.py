from datetime import datetime
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(PostForm, self).__init__(*args, **kwargs)
    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'border-0 p-2 h1 font-weight-light',
                                                          'placeholder': 'Title',
                                                          'autofocus': 'autofocus'}))
    content = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'class': 'col-12 border-0 p-2 h5 font-weight-light',
                                                           'onkeyup': 'autogrow(this);',
                                                           'placeholder': 'What do you think?'}))

    class Meta:
        model = Post
        fields = ['title', 'content']
