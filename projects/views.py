from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


def hello(request):
    """定义函数视图"""
    return HttpResponse("<h1>Hello,大佬们！</h1>")


class ProjectView(View):
    """定义类视图"""

    def get(self, request, pk):
        data = {
            'id': 100,
            'name': 'curry',
            'sex': '男'
        }
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

    def put(self, request):
        return HttpResponse("更新项目信息")

    def post(self, request):
        return HttpResponse(f"创建项目信息")

    def delete(self, request):
        return HttpResponse("删除项目信息")
