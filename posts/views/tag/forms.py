from django import forms

from posts.models import Tag


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator')
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=True,
                                              widget=forms.TextInput(attrs={'class': 'form-control badge-pill',
                                                                            'autofocus': 'autofocus'}))

    class Meta:
        model = Tag
        fields = ['name']
