from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def hello(request):
    return HttpResponse("<h1>Hello,大佬们！</h1>")


def create_project(request):
    return HttpResponse("创建项目信息")


def put_project(request):
    return HttpResponse("更新项目信息")


def get_project(request):
    return HttpResponse("获取项目信息")


def delete_project(request):
    return HttpResponse("删除项目信息")


def id_project(request, pk):
    return HttpResponse(f"删除项目信息{pk}")
