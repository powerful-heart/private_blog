from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    '''
    用户表：User
        username：账号
        password：密码
        data_joined：注册时间
        email: 邮箱
        avatar：图像
        telephone：电话
        blog：博客站点(一对一)
    '''
    avatar = models.FileField(upload_to='avatar/', default='static/img/user.png')
    telephone = models.CharField(max_length=11)
    blog = models.OneToOneField(to='Blog', null=True, on_delete=models.SET_NULL, db_constraint=False)


class Blog(models.Model):
    """
博客站点表：Blog
    site: 站点域名
    name：站点名
    title：标题
    theme：站点主体样式
    category：拥有的分类(多对多)
    tag: 拥有的标签(多对多)
    """
    name = models.CharField(max_length=12, unique=True)
    title = models.CharField(max_length=16)
    site = models.CharField(max_length=32)
    theme = models.CharField(max_length=32)
    category = models.ManyToManyField(to='Category', db_constraint=False)
    tag = models.ManyToManyField(to='Tag', db_constraint=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name


class Category(models.Model):
    """
    分类表：Category
    name：分类名
    """
    name = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    标签表：Tag
    name：标签名
    """
    name = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
文章表：Article
    title：文章标题
    desc：文章摘要
    content：文章内容
    create_time：发布事件
    blog：所属博客站点(一对多)
    category：所属分类(一对多)
    tag：拥有的标签(多对多)
    """
    title = models.CharField(max_length=32, unique=True)
    desc = models.CharField(max_length=256)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(to='Blog', null=True, on_delete=models.SET_NULL, db_constraint=False)
    category = models.ForeignKey(to='Category', null=True, on_delete=models.SET_NULL, db_constraint=False)
    tag = models.ManyToManyField(to='Tag', db_constraint=False)

    # 评论数 , 点赞数, 点踩数
    comment_num = models.IntegerField(default=0)
    up_num = models.IntegerField(default=0)
    down_num = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class UPorDown(models.Model):
    """
    点赞点踩表：UpOrDown  # user与article的点踩关系表
    user：点赞点踩用户(一对多)
    article：点赞点踩文章(一对多)
    is_up：点赞或点踩
    """
    user = models.ForeignKey(to='User', null=True, on_delete=models.SET_NULL, db_constraint=False)
    article = models.ForeignKey(to='Article', null=True, on_delete=models.SET_NULL, db_constraint=False)
    is_up = models.BooleanField()

    def __str__(self):
        return self.user, '给', self.article, '点赞了'

    class Meta:
        unique_together = ('article', 'user')
        verbose_name = '点赞点踩'
        verbose_name_plural = verbose_name


class Common(models.Model):
    '''
    评论表：Common  # user与article的评论关系表
        user：点赞点踩用户(一对多)
        article：点赞点踩文章(一对多)
        content：评论内容
        parent：父评论(自关联, 一对多)
    '''
    user = models.ForeignKey(to='User', null=True, on_delete=models.SET_NULL, db_constraint=False)
    article = models.ForeignKey(to='Article', null=True, on_delete=models.SET_NULL, db_constraint=False)
    content = models.CharField(max_length=128)
    parent = models.ForeignKey(to='self', null=True, on_delete=models.SET_NULL, db_constraint=False)
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user, '给', self.article, '评论了', self.content

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name






