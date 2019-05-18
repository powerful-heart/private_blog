from django.test import TestCase
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bbs.settings')

# Create your tests here.
django.setup()
from blog.models import *
from django.db.models import F,Q
from django.db.models import Avg, Max, Min, Count, Sum

# Create your tests here.


import random
#
# def test(digit_size): # digit_size 自定义验证码位数
#     res = ''
#     for i in range(int(digit_size)):
#         num = str(random.randint(0, 9))  # 随机数字
#         u_alp = chr(random.randint(65, 90)) # 随机大写字母，chr(ASCII小写字符对应数字)
#         l_alp = chr(random.randint(97, 122)) # 随机小写字母
#         res += random.choice([num, u_alp, l_alp]) # 随机三种格式之一，并实现字符串的拼接
#     return res
#
# # i_digit_size = input('请输入随机验证码位数：')
# print(test(4))


# for i in range(6):
#     num = str(random.randint(0, 9))  # 随机数字
#     u_alp = chr(random.randint(65, 90))  # 随机大写字母，chr(ASCII小写字符对应数字)
#     l_alp = chr(random.randint(97, 122))  # 随机小写字母
#     res = random.choice([num, u_alp, l_alp])  # 随机三种格式之一，并实现字符串的拼接
#     print(res)


# print(Article.objects.all())

# 该站点下的分组与该分组下的文章数
# res = Category.objects.filter(blog__user__username__contains='jason').values('name').annotate(Count('name'))
# 该user的站点下的标签
# res = Category.objects.filter(blog__user__username__contains='egon').values('name').annotate('user__blog__name')
# res = Category.objects.filter(blog=4).values('name').filter(article=)

print(res)
