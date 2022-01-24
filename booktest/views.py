from http.client import HTTPResponse
from multiprocessing import context
import re
from tempfile import tempdir
# from tkinter import E
from urllib import response
from urllib.request import Request
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from datetime import datetime,timedelta
from django.template import loader
from booktest.models import BookInfo
from booktest.models import PicTest 
from booktest.models import AreaInfo 
from django.core.paginator import Paginator


def session_set(request):
    request.session['name'] = 'joker'
    return HttpResponse('ok')


def session_get(request):
    name = request.session['name'] 
    return HttpResponse(name)


def areas(request):
    return render(request, 'booktest/areas.html')


def prov(request):
    areas = AreaInfo.objects.filter(aParent__isnull=True) 
    areas_list = list()
    for area in areas:
        areas_list.append((area.id, area.atitle))
    return JsonResponse({'data': areas_list})


def city(request, pid):
    # area = AreaInfo.objects.get(id=pid)
    # areas = area.areainfo_set.all()
    areas = AreaInfo.objects.filter(aParent__id=pid)
    areas_list = list()
    for area in areas:
        areas_list.append((area.id, area.atitle))
    return JsonResponse({'data': areas_list})


def show_area(request, pindex):
    # 如果url设置了分组, 但是没有传参数, django会默认传一个空字符串
    if pindex == '':
        pindex = 1
    areas = AreaInfo.objects.filter(aParent__isnull=True) 
    paginator = Paginator(areas, 10)
    page = paginator.page(int(pindex))
    print(paginator.num_pages)
    print(paginator.page_range)
    print(page.number)
    return render(request, 'booktest/show_area.html', {'page': page})


def show_upload(request):
    return render(request, 'booktest/upload_pic.html')


def upload_handle(request):
    # 1. get pic obj, if pic < 2.5m, file store in memory, else store in a temporary file
    pic = request.FILES['pic']

    # 2. create file
    save_path = '%s/booktest/%s' % (settings.MEDIA_ROOT, pic.name)
    with open(save_path, 'wb') as f:
        # 3. write in file
        for content in pic.chunks():
            f.write(content)

    # 4. write in db
    PicTest.objects.create(goods_pic='booktest/%s' % pic.name)

    # 5. return
    return HttpResponse('ok')

def login_required(view_func):
    '''judge func'''
    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('islogin'):
            return view_func(request, *view_args, **view_kwargs)
        else:
            return redirect('/login')
    return wrapper


def ip_block(view_func):
    '''judge func'''
    def wrapper(request, *view_args, **view_kwargs):
        if request.META['REMOTE_ADDR'] in EXCLUDE_IPS: 
            return render(request, '404.html')
        else:
            return view_func(request, *view_args, **view_kwargs)
    return wrapper


EXCLUDE_IPS = ['192.168.83.1']
@ip_block
def index(request):
    # print(request.method)
    # temp = loader.get_template('booktest/index.html')
    # context = RequestContext(request, {})
    # res_html = temp.render(context)
    # user_ip = request.META['REMOTE_ADDR']
    # if user_ip in EXCLUDE_IPS:
    #     return render(request, '404.html')
    print('index')
    # num = 1 + 'a'
    return render(request, 'booktest/index.html')


def index2(request):
    return render(request, 'booktest/index3.html')
    

def temp_inherit(request):
    return render(request, 'booktest/child.html')


def temp_var(request):
    my_dict = {'title': '字典'}
    my_list = [1, 2, 3]
    book = BookInfo.objects.get(id=1)
    context = {'my_dict': my_dict, 'my_list':my_list, 'book': book}
    return render(request, 'booktest/temp_var.html', context)


def temp_tags(request):
    books = BookInfo.objects.all()
    return render(request, 'booktest/temp_tags.html', {'books': books}) 


def temp_filter(request):
    books = BookInfo.objects.all()
    return render(request, 'booktest/temp_filter.html', {'books': books}) 


def showarg(request, num):
    return HttpResponse(num)


def login(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
    else:
        username = ''
    return render(request, 'booktest/login.html', {'username': username})


def login_check(request):
    # request.POST 保存post提交的参数
    # request.GET 保存get提交的参数
    # print(type(request.POST))
    print(request.method)
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')

    if username == 'smart' and password == '123':
        response = redirect("/index")
        if remember == "on":
            response.set_cookie('username', username, max_age=14*24*3600)
        request.session['islogin'] = True
        request.session['username'] = username 
        return response
    else:
        return redirect("/change_pwd")


def ajax_test(request):
    return render(request, 'booktest/ajax_test.html')


def ajax_handle(request):
    return JsonResponse({"res": 1})


def login_ajax(request):
    return render(request, 'booktest/login_ajax.html')


def ajax_check(request):
    if request.POST.get('username') == 'smart' and request.POST.get('password') == '123':
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


def set_cookie(request):
    response = HttpResponse("设置cookie")
    response.set_cookie('num', 1, max_age=14*24*3600)
    response.set_cookie('num2', 2, max_age=14*24*3600)
    # response.set_cookie('num', 1, expires=datetime.now()+timedelta(days=14))
    return response


def get_cookie(request):
    num = request.COOKIES['num']
    return HttpResponse(num)


def html_escape(request):
    """通过模板上下文传入的特殊字符会被转义"""
    return render(request, 'booktest/html_escape.html', {'content': '<h1>hello</h1>'})


@login_required
def change_pwd(request):
    return render(request, 'booktest/change_pwd.html')


@login_required
def change_pwd_action(request):
    pwd = request.POST.get('pwd')
    username = request.session.get('username')
    return HttpResponse('%s NewPWD:%s' % (username, pwd))


def url_reverse(request):
    return render(request, 'booktest/url_reverse.html')


def show_args(request, a ,b):
    return HttpResponse('%s + %s' % (a, b))


def show_kwargs(request, c ,d):
    return HttpResponse('%s + %s' % (c, d))


from django.core.urlresolvers import reverse
from django.conf import settings


def test_redirect(request):
    # url = reverse('booktest:index')
    # url = reverse('booktest:show_args', args=(1, 2))
    url = reverse('booktest:show_kwargs', kwargs={'c':3, 'd':4})
    return redirect(url)


def static_test(request):
    # ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
    # print(settings.STATICFILES_FINDERS)
    return render(request, 'booktest/static_test.html')
