from django.shortcuts import render, HttpResponse, get_object_or_404
import time, json
from applications.users import models
from django.db.models import Q
from django.views import View
# Create your views here.


def homepage(request):
    '''主页'''
    return render(request, "homepage.html")


def search_view(request):
    '''搜索结果'''
    fish_batch = request.GET.get("fish_batch")
    result = {"fish_batch": fish_batch}
    return render(request, "search_result.html", result)


def adminView(request):
    '''后台管理首页'''
    return render(request, "fishes/fish_admin.html")


def productInfoView(request):
    '''产品信息查看'''
    print("call product info view ", request.META.get("HTTP_X_PJAX", None))
    time.sleep(2)
    return render(request, "fishes/product_info.html")


def userInfoView(request):
    '''用户信息产看'''
    print('in user info')

    if request.GET.get('offset') is None:
        return render(request, "fishes/user_info.html")

    search = request.GET.get('search')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')

    users = None
    if search is not None:
        users = models.GrouperUser.objects.filter(Q(username__contains=search) | Q(employeeID=search))
    else:
        users = models.GrouperUser.objects.all()

    if sort is not None:
        if order == 'asc':
            users = users.order_by('-' + sort)
        else:
            users = users.order_by(sort)

    total = users.count()

    data = []
    for user in users:
        if not user.is_active:
            continue
        last_login = None
        if user.last_login is not None:
            last_login = user.last_login.strftime('%Y-%m-%d %H:%M:%S')
        temp = {
            'id': user.id,
            'username': user.username,
            'employeeID': user.employeeID,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'last_login':  last_login,
        }
        data.append(temp)

    result = {'total': total, 'rows': data[0+int(offset):0+int(offset)+int(limit)]}
    return HttpResponse(json.dumps(result))


def userDetailView(request, uid):
    user = models.GrouperUser.objects.filter(id=uid).first()
    result = {"id": user.id,
              "username": user.username,
              "employeeID": user.employeeID
              }
    return HttpResponse(json.dumps(result))


class AddUserView(View):
    """添加用户信息"""

    def get(self, request):
        return render(request, "fishes/add_user.html")

    def post(self, request):

        result = {"status": False, "message": '添加数据失败，请重试！'}
        employeeID = request.POST.get('val-employeeID')
        username = request.POST.get('val-username')
        password = request.POST.get('val-password')
        phonenum = request.POST.get('val-phonenum')

        is_manager = False
        if request.POST.get('val-is-manager') == '是':
            is_manager = True

        if models.GrouperUser.objects.filter(employeeID=employeeID).exists():
            result['message'] = '该员工号已经存在！'
        else:
            user = models.GrouperUser.objects.create_user(employeeID=employeeID,
                                                          username=username,
                                                          password=password,
                                                          is_superuser=is_manager,
                                                          phoneNum=phonenum)
            if user is not None:
                result['status'] = True
                result['message'] = '添加用户成功！'

        return HttpResponse(json.dumps(result))


def deleteUserView(request):
    employeeIDs = request.POST.getlist('employeeIDs')
    result = {'status': False, 'message': '删除失败，请重试！'}
    for employeeID in employeeIDs:
        user = get_object_or_404(models.GrouperUser, employeeID=employeeID)
        user.is_active = False
        user.save()
    result['status'] = True
    result['message'] = '删除成功！'
    return HttpResponse(json.dumps(result))



def fishPoolInfoView(request):
    '''产看鱼池信息'''
    time.sleep(2)
    return render(request, "fishes/fish_pool_info.html")


def addFishPoolView(request):
    '''添加鱼池信息'''
    time.sleep(2)
    return render(request, "fishes/add_fish_pool.html")


def generateERCodeView(request):
    '''生成产品二维码'''
    time.sleep(1)
    return render(request, "fishes/generate_ERcode.html")


def thirdPartTestReportView(request):
    '''第三方检测报告管理'''
    time.sleep(1)
    return render(request, "fishes/third_part_test_report.html")

def feedbackNOTReplyView(request):
    '''未回复反馈'''
    return render(request, "fishes/feedback_not_reply.html")


def feedbackReplyView(request):
    '''已回复反馈'''
    return render(request, "fishes/feedback_reply.html")


def sysSetForHomepageView(request):
    '''网站首页内容设置'''
    return render(request, "fishes/sysset_for_homepage.html")


def sysSetForSearchResultView(request):
    '''搜索结果页面设置'''
    return render(request, "fishes/sysset_for_serach_result.html")