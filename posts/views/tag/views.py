from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView
from django.db.models import Q
from django.utils.text import slugify

from posts.models import Tag, Post
from posts.definitions import Status
from posts.views.tag.forms import TagForm
from posts.views.tag.decorators import collection, name_process


@method_decorator(login_required, name='dispatch')
class TagBoxView(ListView):
    model = Tag
    template_name = 'tag/box.html'
    
    def dispatch(self, request, *args, **kwargs):
        collection()
        return super(TagBoxView, self).dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        collection()
        return super(TagAddView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form'] = TagForm(creator=self.request.user)
        return super(TagAddView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = self.request.user
        if user.is_superuser:
            form.instance.is_public = True
        else:
            form.instance.creator = user
        name = name_process(form.instance.name)
        form.instance.name = name
        form.instance.slug = slugify(form.instance.name)
        form.save()
        return super(TagAddView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class TagPostsView(DetailView):
    model = Tag
    template_name = 'tag/posts.html'

    def dispatch(self, request, *args, **kwargs):
        collection()
        return super(TagPostsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['posts'] = Post.objects.filter(tags__name__contains=self.get_object(), status=Status.Published.value[0])
        return super(TagPostsView, self).get_context_data(**kwargs)
