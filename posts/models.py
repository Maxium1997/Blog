from django.db import models
from django.urls import reverse

from .definitions import Status
from accounts.models import User
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()
    is_public = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('tag_box')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='posts')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.PositiveSmallIntegerField(default=Status.Saved.value[0])
    published_time = models.DateTimeField(null=True)
    updated_time = models.DateTimeField(null=True)
    tags = models.ManyToManyField(Tag)

    def get_absolute_url(self):
        return reverse('my_drafts')

    def __str__(self):
        return self.title

    def image_upload(self, photo):
        self.image.save(self.author.username+'/'+self.title+'/'+'{}'.format(photo),
                        photo,
                        save=True)
        self.save()


class Message(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    content = models.TextField()
    published_time = models.DateTimeField(auto_now_add=True)


class Comment(Message):
    source = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)


class SubComment(Message):
    source = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False)
