from django.urls import path, include

from .views.post.views import IndexView, PublicPostsView, \
    MyDraftsView, MyPublicPostsView, MyPrivacyPostView, PostDetailView, \
    PostCreateView, PostUpdateView, PostDeleteView, \
    post_publish, post_tags_clear, \
    post_comment
from .views.tag.views import TagBoxView, TagAddView, TagPostsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts', PublicPostsView.as_view(), name='posts'),
    path('<pk>', PostDetailView.as_view(), name='post_detail'),

    path('my/', include([
        path('posts/', include([
            path('drafts', MyDraftsView.as_view(), name='my_drafts'),
            path('public', MyPublicPostsView.as_view(), name='my_public'),
            path('privacy', MyPrivacyPostView.as_view(), name='my_privacy'),
            path('new', PostCreateView.as_view(), name='new_post'),
            path('<pk>/', include([
                path('edit', PostUpdateView.as_view(), name='post_edit'),
                path('tags_clear', post_tags_clear, name='post_tags_clear'),
                path('publish', post_publish, name='post_publish'),
                path('delete', PostDeleteView.as_view(), name='post_delete'),
                path('comment', post_comment, name='post_comment'),
            ]))
        ])),

        path('tags/', include([
            path('box', TagBoxView.as_view(), name='tag_box'),
            path('add', TagAddView.as_view(), name='tag_add'),
            path('<slug>', TagPostsView.as_view(), name='tag_posts'),
        ]))
    ]))
]
