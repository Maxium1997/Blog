from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .models import Post
from .definitions import Status
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


@method_decorator(login_required, name='dispatch')
class MyDraftsView(TemplateView):
    template_name = 'posts/drafts.html'

    def get_context_data(self, **kwargs):
        kwargs['drafts'] = Post.objects.filter(author=self.request.user, status=Status.Saved.value[0])
        return super(MyDraftsView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class MyPublicPostsView(TemplateView):
    template_name = 'posts/drafts.html'

    def get_context_data(self, **kwargs):
        kwargs['public_posts'] = Post.objects.filter(author=self.request.user, status=Status.Published.value[0])
        return super(MyPublicPostsView, self).get_context_data(**kwargs)
