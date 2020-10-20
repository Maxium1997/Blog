from django.shortcuts import render
from django.views.generic import TemplateView

from posts.models import Post
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs['posts'] = Post.objects.all()
        return super(IndexView, self).get_context_data(**kwargs)
