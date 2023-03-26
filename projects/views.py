import json
from django.db.models import Q, QuerySet, Count, Avg, Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .models import Projects
from interfaces.models import Interfaces
# Create your views here.
from django.views import View
from django.db import connection
from .serializers import ProjectSerializer, ProjectModelSerializer


class ProjectView(GenericAPIView):
    """
    继承GenericAPIView父类(GenericAPIView子类)
    a.具备View的所有特性
    b.具备了APIView中的认证、授权、限流功能
    c.还支持对于获取列表数据接口的功能:搜索、排序、分页
    """
    """
    一旦继承GenericAPIView之后，往往需要指定queryset、serializer_class类属性
    queryset指定当前类视图的实例方法需要使用的查询集对象
    serializer_class指定当前类视图的实例方法需要使用的序列化器类
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

    """获取所以项目信息"""

    def get(self, request: Request):
        """
        1、在实例方法中，往往使用get_queryset()方法获取查询集对象
        2、一般不会指定调用queryset类属性,原因:为了提供让用户重写get_queryset()
        3、如果未重写get_queryset()方法，那么必须得指定queryset类属性

        1、在实例方法中，往往使用get_serializer()方法获取序列化器类
        2、一般不会指定调用serializer_class类属性，原因:为了提供让用户重写get_serializer_class()
        3、如果未重写get_serializer_class()方法，那么必须得指定serializer_class类属性
        """
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """创建项目信息"""

    def post(self, request):
        req_ser = self.get_serializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        req_ser.save()
        return Response(req_ser.data, status=status.HTTP_201_CREATED)


class ProjectViewId(GenericAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    """
    a.lookup_url_kwarg默认为None
    b.如果lookup_url_kwarg为None，那么lookup_url_kwarg与lookup_field相同("PK")
    c.lookup_url_kwarg指定url路由条目中外键的路径参数名称
    """
    lookup_url_kwarg = "id"

    """def get_obj(self, pk):
        project_obj = self.get_queryset().get(id=pk)
        return project_obj"""

    """获取所以单笔项目信息"""

    def get(self, request, **kwargs):
        """
        project_obj = self.get_object (pk)
        get_object可以获取模型对象，无需传递外键值
        """
        project_obj = self.get_object()
        serializer = self.get_serializer(instance=project_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """更新项目信息"""

    def put(self, request, **kwargs):
        project_d = self.get_object()
        req_ser = self.get_serializer(instance=project_d, data=request.data)
        req_ser.is_valid(raise_exception=True)
        req_ser.save()
        return Response(req_ser.data, status=status.HTTP_201_CREATED)

    """删除项目信息"""

    def delete(self, request, **kwargs):
        self.get_object().delete()
        return Response({"删除项目信息": "ok"}, status=status.HTTP_204_NO_CONTENT)
