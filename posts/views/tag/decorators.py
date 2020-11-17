import collections
from posts.models import Tag


def collection():
    all_tags_name = [tag.name for tag in Tag.objects.all()]
    repeat_names_list = [item for item, count in collections.Counter(all_tags_name).items() if count > 1]
    for repeat_name in repeat_names_list:
        tags = Tag.objects.filter(name=repeat_name)
        tag = Tag.objects.get(id=tags[0].id)
        tag.is_public = True
        tag.creator = None
        tag.save()
        for tag in tags[1:]:
            tag.delete()


def name_process(origin_name: str):
    word_list = origin_name.strip().split(' ')
    name = ''
    for word in word_list:
        name += word[0].upper() + word[1:]
    return name
