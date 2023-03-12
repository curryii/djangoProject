from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Projects
# Create your views here.
from django.views import View
from django.db import connection


def hello(request):
    """定义函数视图"""
    return HttpResponse("<h1>Hello,大佬们！</h1>")


class ProjectView(View):
    """定义类视图"""

    def get(self, request, pk):
        data = [{
            'id': pk,
            'name': 'curry',
            'sex': '男'
        },
            {
                'id': pk,
                'name': 'curry',
                'sex': '男'
            },
            {
                'id': pk,
                'name': 'curry',
                'sex': '男'
            }]
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, safe=False)

    def put(self, request):
        return HttpResponse("更新项目信息")

    def post(self, request, pk):
        print(pk)
        return HttpResponse(f"创建项目信息")

    def delete(self, request):
        return HttpResponse("删除项目信息")


def sql(request):
    """创建方式一"""
    # obj = Projects(name="java项目", leader="curry")
    # obj.save()
    """创建方式二"""
    # obj = Projects.objects.create(name="JS项目", leader="FFF")
    """查询多条数据方式一"""
    # qs = Projects.objects.all()
    """查询单条数据方式一"""
    # obj = Projects.objects.get(name="java项目")
    """查询单条数据方式二"""
    # obj = Projects.objects.filter(leader="xin_pro").filter()
    # obj = Projects.objects.filter(leader="xin_pro").first()
    # obj = Projects.objects.filter(leader="xin_pro").last()
    # obj = len(Projects.objects.filter(leader="xin_pro"))
    # obj = Projects.objects.filter(leader="xin_pro").count()
    obj = "null"
    return JsonResponse({"msg": f"{obj}"})
