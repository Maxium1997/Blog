from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .models import Tag


@method_decorator(login_required, name='dispatch')
class TagBoxView(ListView):
    model = Tag
    template_name = 'tag/box.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        kwargs['tag_box'] = user.box.tags.all()
        return super(TagBoxView, self).get_context_data(**kwargs)
