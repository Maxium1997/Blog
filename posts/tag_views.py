from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView
from django.db.models import Q
from django.utils.text import slugify

from .models import Tag, Post
from .tag_forms import TagForm


@method_decorator(login_required, name='dispatch')
class TagBoxView(ListView):
    model = Tag
    template_name = 'tag/box.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        filter_criteria = Q(is_public=True) | Q(creator=user)
        kwargs['tag_box'] = Tag.objects.filter(filter_criteria)
        return super(TagBoxView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class TagAddView(CreateView):
    model = Tag
    fields = ['name']
    template_name = 'tag/add.html'

    def get_context_data(self, **kwargs):
        kwargs['form'] = TagForm(user=self.request.user)
        return super(TagAddView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = self.request.user
        if user.is_superuser:
            form.instance.is_public = True
        else:
            form.instance.creator = user
        form.instance.slug = slugify(form.instance.name)
        form.save()
        return super(TagAddView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class TagPostsView(DetailView):
    model = Tag
    template_name = 'tag/posts.html'

    def get_context_data(self, **kwargs):
        kwargs['posts'] = Post.objects.filter(tags__name__contains=self.get_object())
        return super(TagPostsView, self).get_context_data(**kwargs)
