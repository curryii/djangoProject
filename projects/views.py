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
from rest_framework import filters
from .serializers import ProjectSerializer, ProjectModelSerializer
from utils.pagination import PageNumberPagination
from rest_framework import mixins

# Mixin拓展类
"""class ListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)"""

"""class CreateModelMixin:
    def create(self, request, *args, **kwargs):
        req_ser = self.get_serializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        req_ser.save()
        return Response(req_ser.data, status=status.HTTP_201_CREATED)"""


class ProjectView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericAPIView
):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "^name", "=leader"]
    pagination_class = PageNumberPagination

    ordering_fields = ["id", "name", "leader"]

    """获取所以项目信息"""

    def get(self, request, *args, **kwargs):
        """queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)"""
        """
        a. python中支持多重继承，一个类可以同时继承多个父类
        b.类中的方法和属性是按照_mro_所指定的继承顺序进行搜索
        """
        return self.list(request, *args, **kwargs)

    """创建项目信息"""

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProjectViewId(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer

    lookup_url_kwarg = "id"

    """获取所以单笔项目信息"""

    def get(self, request, *args, **kwargs):
        """project_obj = self.get_object()
        serializer = self.get_serializer(instance=project_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)"""
        return self.retrieve(request, *args, **kwargs)

    """更新项目信息"""

    def put(self, request, *args, **kwargs):
        """project_d = self.get_object()
        req_ser = self.get_serializer(instance=project_d, data=request.data)
        req_ser.is_valid(raise_exception=True)
        req_ser.save()
        return Response(req_ser.data, status=status.HTTP_201_CREATED)"""
        return self.update(request, *args, **kwargs)

    """删除项目信息"""

    def delete(self, request, *args, **kwargs):
        """self.get_object().delete()
        return Response({"删除项目信息": "ok"}, status=status.HTTP_204_NO_CONTENT)"""
        return self.destroy(request, *args, **kwargs)
