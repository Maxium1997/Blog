from datetime import datetime
from django import forms
from django.db.models import Q

from posts.models import Post, Tag, Comment


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['tags'] = forms.ModelMultipleChoiceField(
            required=True,
            queryset=Tag.objects.filter(Q(is_public=True) | Q(creator=self.author)),
            widget=forms.CheckboxSelectMultiple,
        )
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
        fields = ['title', 'content', 'tags']


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop('source')
        self.commenter = kwargs.pop('user')

        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(required=True,
                                                widget=forms.TextInput(attrs={'class': 'form-control m-2'}))
        self.fields['content'] = forms.CharField(required=True,
                                                 widget=forms.Textarea(attrs={'class': 'form-control m-2'}))

    def save(self, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.source = self.source
        try:
            comment.commenter = self.commenter
        except ValueError:
            comment.commenter = None

        if commit:
            comment.save()
        return comment

    class Meta:
        model = Comment
        fields = ['email', 'content']
