from datetime import datetime
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView

from .models import Post
from .definitions import Status
from .forms import PostForm
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
    template_name = 'posts/public.html'

    def get_context_data(self, **kwargs):
        kwargs['public_posts'] = Post.objects.filter(author=self.request.user, status=Status.Published.value[0])
        return super(MyPublicPostsView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class MyPrivacyPostView(TemplateView):
    template_name = 'posts/privacy.html'
    
    def get_context_data(self, **kwargs):
        kwargs['privacy_posts'] = Post.objects.filter(author=self.request.user, status=Status.Privacy.value[0])
        return super(MyPrivacyPostView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'posts/create.html'

    def get_context_data(self, **kwargs):
        kwargs['form'] = PostForm(author=self.request.user)
        return super(PostCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.updated_time = datetime.now()
        form.save()
        return super(PostCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'tags']
    template_name = 'posts/edit.html'

    def get_context_data(self, **kwargs):
        post = super(PostUpdateView, self).get_object()
        kwargs['form'] = PostForm(instance=post, author=self.request.user)
        kwargs['status'] = Status.__members__
        return super(PostUpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.updated_time = datetime.now()
        form.save()
        return super(PostUpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    success_url = reverse_lazy('my_drafts')


class PostDetailView(TemplateView):
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):
        kwargs['post'] = Post.objects.get(pk=kwargs['pk'])
        return super(PostDetailView, self).get_context_data(**kwargs)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        raise PermissionError
    else:
        post.status = Status.Published.value[0]
        post.published_time = datetime.now()
        post.save()
        messages.success(request, "Your post has published, you can share with everyone.")
        return redirect('my_public')


@login_required
def post_tags_clear(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        raise PermissionError
    else:
        post.tags.clear()
        return redirect('my_drafts')
