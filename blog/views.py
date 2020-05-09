import time

from django.shortcuts import render,redirect,reverse
from django.http import  HttpResponse

from .models import Article, Category, Banner, Tag, Link
# 导入分页插件包
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 欢迎页
def welcome(request):
    return render(request, "welcome.html")


# 首页
def index(request):
    # 查询所有分类
    all_category = Category.objects.all()
    # 查询所有激活状态幻灯图数据，并进行切片
    banners = Banner.objects.filter(is_active=True)[0:4]
    # 查询推荐位为推门推荐的文章
    tui_articles = Article.objects.filter(tui__id=2)[:3]
    # 查询最新10条文章
    new_articles = Article.objects.all().order_by('-id')[0:10]
    # 热门文章排行通过浏览数进行排序
    hot = Article.objects.all().order_by('views')[:10]
    # 热门推荐
    remen = Article.objects.filter(tui__id=2)[:6]
    # 标签
    tags = Tag.objects.all()
    # 友情链接
    link = Link.objects.all()
    centent = {
        'all_category': all_category,
        'banners': banners,
        'tui_articles': tui_articles,
        'new_articles': new_articles,
        'hot': hot,
        'remen': remen,
        'tags': tags,
        'link': link
    }
    return render(request, 'blog/index.html', centent)


# 列表页
def list(request, lid):
    # 查询所有分类
    all_category = Category.objects.all()
    # 获取通过URL传进来的lid，然后筛选出对应文章
    list = Article.objects.filter(category_id=lid)
    # 获取当前文章的栏目名
    cname = Category.objects.get(id=lid)
    # 右侧的热门推荐
    remen = Article.objects.filter(tui__id=2)[:6]
    # 右侧所有文章标签
    tags = Tag.objects.all()
    # 在URL中获取当前页面数
    page = request.GET.get('page')
    # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    paginator = Paginator(list, 2)
    try:
        # 获取当前页码的记录
        list = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户输入的页码不是整数时,显示第1页的内容
        list = paginator.page(1)
    except EmptyPage:
        # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        list = paginator.page(paginator.num_pages)
    return render(request, 'blog/list.html', locals())


# 内容页
def show(request, sid):
    # 查询所有分类
    all_category = Category.objects.all()
    # 查询指定ID的文章
    show = Article.objects.get(id=sid)
    # 右侧所有标签
    tags = Tag.objects.all()
    # 右侧热门推荐
    remen = Article.objects.filter(tui__id=2)[:6]
    # 内容下面的您可能感兴趣的文章，随机推荐
    hot = Article.objects.all().order_by('?')[:10]
    previous_blog = Article.objects.filter(created_time__gt=show.created_time, category=show.category.id).first()
    netx_blog = Article.objects.filter(created_time__lt=show.created_time, category=show.category.id).last()
    show.views = show.views + 1
    show.save()
    return render(request, 'blog/show.html', locals())


# 标签页
def tag(request, tag):
    pass


# 搜索页
def search(request):
    ss = request.GET.get('search')  # 获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)  # 获取到搜索关键词通过标题进行匹配
    remen = Article.objects.filter(tui__id=2)[:6]
    all_category = Category.objects.all()
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'blog/search.html', locals())


# 关于我们
def about(request):
    # return HttpResponse("博主很懒，什么都没有留下！")
    return redirect(reverse(index))