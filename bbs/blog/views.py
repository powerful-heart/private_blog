from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from blog import myform
from blog.models import User, Article, Category, Tag, Blog, UPorDown,Common
# Image生成纯色图片, ImageDraw在图片上写字, ImageFont字体
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO, StringIO
import random,os, json
from django.contrib import auth
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import F

# Create your views here.

# 定义接口规范
response_dic = {
    'status': 1,
    'msg': 'ok',
    'data': {}
}


def home(request):
    article_list = Article.objects.all().order_by('-pk')
    paginator = Paginator(article_list, 4)
    count = paginator.count
    num_pages = paginator.num_pages
    # 页码列表
    page_range = paginator.page_range  # type:int
    print(page_range)
    try:
        current_num = int(request.GET.get('page', 1))
    except:
        current_num = 1
    print('当前页数', current_num)
    # 不在页面范围内的安全处理
    if current_num < 1:
        current_num = 1
        return redirect('/home/?page=%s' % current_num)
    elif current_num > num_pages:
        current_num = num_pages
        return redirect('/home/?page=%s' % current_num)

    current_page = paginator.page(current_num)
    print('>>>', current_page)

    # 通过page_range来控制页面版面
    if num_pages > 10:
        if current_num < 4:
            page_range = range(2, 5)
        elif current_num > num_pages - 3:
            page_range = range(num_pages - 3, num_pages)
        else:
            page_range = range(current_num - 1, current_num + 2)

    return render(request, 'home.html', locals())


def register(request):
    if request.method == 'GET':
        my_form = myform.Myform()
        return render(request, 'register.html', locals())
    elif request.method == 'POST':
        # 获取头像
        avatar = request.FILES.get('myfile', None)
        my_form = myform.Myform(request.POST)
        if my_form.is_valid():
            cleaned_form = my_form.cleaned_data
            cleaned_form.pop('re_password')
            # 判断用户是否上传头像, 是则加入cleaned_form
            if avatar:
                cleaned_form['avatar'] = avatar
                # print(cleaned_form)
            user = User.objects.create_user(**cleaned_form)
            if user:
                blog = Blog.objects.create(
                    site=user.username,
                    title=user.username + "的站点",
                    theme=user.username + '.css',
                    # 接口：后期添加个人中心界面，来修改或添加分类们与标签们
                )
                theme_path = 'static/css/%s.css' % user.username
                with open(theme_path, 'wt') as f:
                    f.write('.head{height: 80px;background-color: #2e6da4;}')
                return JsonResponse({
                    'status': 1,
                    'msg': '注册成功',
                    'url': '/login/',
                    'data': {}
                })
            return JsonResponse({
                'status': 2,
                'msg': '注册失败',
                'data': {}
            })
        else:
            return JsonResponse({
                'status': 2,
                'msg': my_form.errors,
                'data': {}
            })
    # return render(request, "register.html", locals())


def login(request):
    if request.method == 'GET':
        next_url = request.GET.get('next', 0)
        print(next_url)
        return render(request, 'login.html', locals())
    elif request.method == 'POST':
        # print(request.POST)
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        auth_code = request.POST.get('auth_code', 'N')
        # 用GET获取next数据
        next_url = request.GET.get('next', '/')
        print(next_url)
        # if request.session.get('auth_code').upper() == auth_code.upper():
        user = auth.authenticate(username=name, password=pwd)
        if user:
            auth.login(request, user)
            response_dic['msg'] = '登陆成功'
            response_dic['url'] = ''+next_url
            print(response_dic)
            # return redirect('/home/')
        else:
            response_dic['msg'] = '用户名或密码错误'
            response_dic['status'] = 2
        # else:
        #     response_dic['status'] = 2
        #     response_dic['msg'] = '验证码错误'
        return JsonResponse(response_dic)


# 获取三原色的数字元组
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# 获取随机图片验证码
def get_code(request):
    # 一、写死了
    # with open('avatar/紫霞仙子.jpg', 'rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 二、不想保存在文件中
    # img = Image.new('RGB', (350, 50), color='red')
    # with open('code.png', 'wb') as f:
    #     img.save(f, 'png')
    # with open('code.png', 'rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 三、 保存在内存管理器中
    # f = BytesIO()
    # img = Image.new('RGB', (350, 50), color='green')
    # # 把文件保存在内存管理器中
    # img.save(f, 'png')
    # return HttpResponse(f.getvalue())
    # 生成带文字的图片

    f = BytesIO()
    img = Image.new('RGB', (350, 50), color=get_random_color())
    img_draw = ImageDraw.Draw(img)
    # 获取字体对象(字体文件 , 字体大小)
    img_font = ImageFont.truetype('static/font/kumo.ttf', size=50)
    # 随机字体
    auth_code = ''
    for i in range(6):
        num = str(random.randint(0, 9))  # 随机数字
        u_alp = chr(random.randint(65, 90))  # 随机大写字母，chr(ASCII小写字符对应数字)
        l_alp = chr(random.randint(97, 122))  # 随机小写字母
        res = random.choice([num, u_alp, l_alp])  # 随机三种格式之一，并实现字符串的拼接
        img_draw.text((30 + i * 50, -8), res, get_random_color(), font=img_font)
        auth_code += res
    request.session['auth_code'] = auth_code
    img.save(f, 'png')
    return HttpResponse(f.getvalue())


# 注销用户
def logout(request):
    auth.logout(request)
    return redirect('/')


# 错误界面
def error(request):
    return render(request, 'error.html')


# 个人站点
def site(request, username, group=None, key=None):
    # print('111', username)
    user = User.objects.filter(username=username).first()  # type:User
    if user:
        blog = user.blog
        article_list = blog.article_set.all().order_by('-pk')
        # 分页器
        paginator = Paginator(article_list, 4)
        count = paginator.count
        num_pages = paginator.num_pages
        # 页码列表
        page_range = paginator.page_range  # type:int
        try:
            current_num = int(request.GET.get('page', 1))
        except:
            current_num = 1
        print('当前页数', current_num)
        # 不在页面范围内的安全处理
        if current_num < 1:
            current_num = 1
            return redirect('/site/?page=%s' % current_num)
        elif current_num > num_pages:
            current_num = num_pages
            return redirect('/site/?page=%s' % current_num)

        current_page = paginator.page(current_num)
        print('>>>', current_page)

        # 通过page_range来控制页面版面
        if num_pages > 10:
            if current_num < 4:
                page_range = range(2, 5)
            elif current_num > num_pages - 3:
                page_range = range(num_pages - 3, num_pages)
            else:
                page_range = range(current_num - 1, current_num + 2)
        # 站点分组, 分组下的文章数
        # category_set = blog.article_set.values('category').annotate(c=Count('title')).values_list('category__name', 'c')
        # print(category_set)
        # tag_set = blog.article_set.values('tag').annotate(c=Count('title')).values_list('tag__name', 'c')
        # print('标签:', tag_set)
        # time_set = blog.article_set.all().annotate(month=TruncMonth('create_time')).\
        #     values('month').annotate(c=Count('pk')).order_by('-month')
        # print('文章档案:', time_set)
        if group and key:
            print(key)
            if group == 'category':
                current_page = article_list.filter(category__name=key)
                print(article_list)
            elif group == 'tag':
                current_page = article_list.filter(tag__name=key)
            else:
                times = key.split('-')
                print('hello', times)
                current_page = article_list.filter(create_time__year=times[0], create_time__month=times[1])

        return render(request, 'site/site.html', locals())
    return render(request, 'error.html')


# 后台管理
@login_required(login_url='/login/')
def backcontrol(request):
    article_list = Article.objects.filter(blog=request.user.blog).order_by('-pk')
    return render(request, 'background/backcontrol.html', {'article_list': article_list})


# 添加文章
def add_article(request):
    if request.method == 'GET':
        category_list = Category.objects.filter(blog=request.user.blog).order_by('pk')
        tag_list = Tag.objects.filter(blog=request.user.blog).order_by('pk')
        return render(request, 'background/add_article.html', locals())
    elif request.method == 'POST':
        print(request.POST)

        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        category_id = request.POST.get('category_id', None)
        tag_ids = request.POST.getlist('tag_id', None)

        # 利用bs4模块解析html文本 , 避免xss攻击
        soup = BeautifulSoup(content, 'html.parser')
        desc = soup.text.strip()[0:100]  # 解析后数据存放在soup.text

        article = Article.objects.create(
            title=title,
            content=content,
            desc=desc,
            blog=request.user.blog,
            category_id=category_id,
        )
        # 多对多添加属性
        print('tags>>>', tag_ids)
        article.tag.add(*tag_ids)
        return redirect('/backcontrol/')


# 编辑文章添加图片(想让这个视图函数局部禁用csrf)
@csrf_exempt
def add_picture(request):
    print('添加图片', request.FILES)
    path = 'media/img'
    if not os.path.exists(path):
        os.mkdir(path)
    file = request.FILES.get('imgFile', None)
    img_path = path + '/' + file.name
    with open(img_path, 'wb') as f:
        for line in file:
            f.write(line)
    return JsonResponse({
        'error': 0,
        'url': '/' + img_path
    })


# 文章内容展示
def article_detail(request, username, article_id):
    user = User.objects.filter(username=username).first()
    blog = user.blog
    article = Article.objects.filter(pk=article_id).first()  # type:Article
    if not blog or not article:
        return render(request, 'error.html')
    if request.user.is_authenticated():
        print(request.user)
        is_up = request.user.upordown_set.filter(article=article).values('is_up').first()
        comment_list = Common.objects.filter(article=article).all()
    return render(request, 'site/site_article.html', locals())


# 点赞点踩
def upordown(request):
    if not request.user.is_authenticated():
        return JsonResponse({
            'status': 2,
            'msg': '请先登录',
            'data': {}
        })
    user = request.user  # 登录时将用户添加到了cession
    is_up = request.GET.get('is_up', None)
    is_up = json.loads(is_up)
    article_id = request.GET.get('article_id', None)

    # 获取当前用户赞踩过得文章
    res = user.upordown_set.filter(article_id=article_id)

    try:
        with transaction.atomic():  # 捕获事物原子性, 一旦异常就会回滚
            if not res:
                if is_up:
                    Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                else:
                    Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                UPorDown.objects.create(user=user, article_id=article_id, is_up=is_up)
            else:
                if is_up:
                    Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                    Article.objects.filter(pk=article_id).update(down_num=F('down_num') - 1)
                else:
                    Article.objects.filter(pk=article_id).update(up_num=F('up_num') - 1)
                    Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                UPorDown.objects.filter(user=user, article_id=article_id).update(is_up=is_up)
    except:
        return JsonResponse({
            'status': 2,
            'msg': 'error',
            'data': {}
        })

    return JsonResponse(response_dic)


# 添加评论
def add_comment(request):
    if not request.user.is_authenticated():
        return JsonResponse({
            'status': 2,
            'msg': '请先登录',
            'data': {}
        })
    user = request.user
    article_id = request.POST.get('article_id', None)
    content = request.POST.get('content', None)
    parent_id = request.POST.get('parent_id', None)

    with transaction.atomic():
        Article.objects.filter(pk=article_id).update(comment_num=F('comment_num') + 1)
        Common.objects.create(user=user, article_id=article_id, content=content, parent_id=parent_id)

    return JsonResponse(response_dic)
























