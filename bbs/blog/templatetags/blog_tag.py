from django.template import Library

from django.db.models import Count
from django.db.models.functions import TruncMonth

register = Library()


@register.inclusion_tag('site/menu_list.html', name='menu_list_tag')
def menu_list(blog):
    category_set = blog.article_set.values('category').annotate(c=Count('title')).values_list('category__name', 'c')
    print('分组:', category_set)
    tag_set = blog.article_set.values('tag').annotate(c=Count('title')).values_list('tag__name', 'c')
    print('标签:', tag_set)
    time_set = blog.article_set.all().annotate(month=TruncMonth('create_time')). \
        values('month').annotate(c=Count('pk')).order_by('-month')
    print('文章档案:', time_set)

    return {
        'category_set': category_set,
        'tag_set': tag_set,
        'time_set': time_set
    }