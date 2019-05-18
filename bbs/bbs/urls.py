"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog import views
from django.views.static import serve
from bbs import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 首页
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home),
    # 注册
    url(r'^register/$', views.register),
    # 登录
    url(r'^login/$', views.login),
    # 后台管理
    url(r'^backcontrol/$', views.backcontrol),
    # 添加文章
    url(r'^add_article/$', views.add_article),
    # 编辑文章添加图片
    url(r'^add_picture/$', views.add_picture),
    # 文章详情
    url(r'^(?P<username>\w+)/article/(?P<article_id>\d+).html$', views.article_detail),
    # 点赞点踩
    url(r'^upordown/$', views.upordown),
    # 添加评论
    url(r'^add_comment/$', views.add_comment),
    # 注销用户
    url(r'^logout/$', views.logout),
    # 获取登录随机验证码
    url(r'^get_code/$', views.get_code),
    # 设置公开资源默认路径
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    # 文章分类展示
    url(r'^(?P<username>\w+)/(?P<group>category|tag|archive)/(?P<key>.+)$', views.site),
    # 个人站点
    url(r'^(?P<username>\w+)/$', views.site),

    url(r'.*/$', views.error),

]
