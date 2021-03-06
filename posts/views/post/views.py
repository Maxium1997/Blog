from datetime import datetime
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView

from posts.models import Post
from posts.definitions import Status
from posts.views.post.forms import PostForm, CommentForm
from posts.views.tag.forms import TagForm
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class PublicPostsView(TemplateView):
    template_name = 'post/index.html'

    def get_context_data(self, **kwargs):
        kwargs['posts'] = Post.objects.filter(status=Status.Published.value[0]).order_by('published_time')
        return super(PublicPostsView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class MyDraftsView(TemplateView):
    template_name = 'post/drafts.html'

    def get_context_data(self, **kwargs):
        kwargs['drafts'] = Post.objects.filter(author=self.request.user, status=Status.Saved.value[0])
        return super(MyDraftsView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class MyPublicPostsView(TemplateView):
    template_name = 'post/public.html'

    def get_context_data(self, **kwargs):
        kwargs['public_posts'] = Post.objects.filter(author=self.request.user, status=Status.Published.value[0])
        return super(MyPublicPostsView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class MyPrivacyPostView(TemplateView):
    template_name = 'post/privacy.html'

    def get_context_data(self, **kwargs):
        kwargs['privacy_posts'] = Post.objects.filter(author=self.request.user, status=Status.Privacy.value[0])
        return super(MyPrivacyPostView, self).get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'tags']
    template_name = 'post/create.html'

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
    template_name = 'post/edit.html'

    def get_context_data(self, **kwargs):
        post = super(PostUpdateView, self).get_object()
        kwargs['form'] = PostForm(instance=post, author=self.request.user)
        kwargs['post'] = self.get_object()
        kwargs['tag_form'] = TagForm(creator=self.request.user)
        kwargs['status'] = Status.__members__
        return super(PostUpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.updated_time = datetime.now()
        form.save()
        return super(PostUpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post/delete.html'
    success_url = reverse_lazy('my_drafts')


class PostDetailView(TemplateView):
    template_name = 'post/detail.html'

    def get_context_data(self, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        kwargs['post'] = post
        kwargs['comment_form'] = CommentForm(source=post, user=self.request.user)
        kwargs['author_related_posts'] = Post.objects.filter(author=post.author, status=Status.Published.value[0]).exclude(pk=post.pk)[:5]
        try:
            kwargs['tag_related_posts'] = post.tags.all().first().post_set.all().filter(status=Status.Published.value[0]).exclude(pk=post.pk)[:5]
        except:
            kwargs['tag_related_posts'] = None
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


def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user:
        CommentForm(request.POST, source=post, user=request.user).save()
    else:
        CommentForm(request.POST, source=post).save()

    return redirect('post_detail', pk=post.pk)
