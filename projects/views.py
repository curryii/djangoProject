import json
from django.db.models import Q, QuerySet, Count, Avg, Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from .models import Projects
from interfaces.models import Interfaces
# Create your views here.
from django.views import View
from django.db import connection
from .serializers import ProjectSerializer, ProjectModelSerializer


def hello(request):
    """定义函数视图"""
    return HttpResponse("<h1>Hello,大佬们！</h1>")


class ProjectView(APIView):
    """获取所以项目信息"""

    def get(self, request):
        res = Projects.objects.all()
        """序列化输出"""
        serializer = ProjectModelSerializer(instance=res, many=True)
        return JsonResponse(serializer.data, safe=False)

    """创建项目信息"""

    def post(self, request):
        """反序列化输入"""
        req_data = json.loads(request.body)
        req_ser = ProjectModelSerializer(data=req_data)

        if not req_ser.is_valid():
            return JsonResponse(req_ser.errors, status=400)

        """
        req_ser.save() == Projects.objects.create(**req_ser.validated_data)
        1、如果在创建序列化器对象时，仅传递data参数，使用序列化器对象调用save方法时，会自动调用序列化器中的create方法
        2、create方法用于对数据进行创建操作
        3、序列化器类中的create方法，validated_data参数为校验通过之后的数据（一般字典类型)
        4、在调用save方法时，可以传递任意的关键字参数，并且会自动合并到validated_data字典中
        5、create方法一般需要将创建成功之后模型对象返回
        """
        req_ser.save()

        """序列化输出
        serializer = ProjectSerializer(instance=projects_obj)
        1、在创建序列化器对象时，仅仅只传递data参数，那么必须得调用is_valid()方法通过之后
        2、如果没有调用save方法，使用创建序列化器对象. data属性，来获取序列化输出的数据
            (会把validated_data数据作为输入源，参照序列化器字段的定义来进行输入)
        3、如果调用了save方法，使用创建序列化器对象.data属性，来获取序列化输出的数据
            (会把create方法返回的模型对象数据作为输入源，参照序列化器字段的定义来进行输出)
        """
        return JsonResponse(req_ser.data, status=201)


class ProjectViewId(View):
    """获取所以单笔项目信息"""

    def get(self, request, pk):
        project_obj = Projects.objects.get(id=pk)
        """序列化输出"""
        serializer = ProjectSerializer(instance=project_obj)
        return JsonResponse(serializer.data)

    """更新项目信息"""

    def put(self, request, pk):
        req_data = json.loads(request.body)
        project_d = Projects.objects.get(id=pk)
        req_ser = ProjectSerializer(instance=project_d, data=req_data)

        if not req_ser.is_valid():
            return JsonResponse(req_ser.errors, status=400)
        """
        1、如果在创建序列化器对象时，同时instance和data参数，使用序列化器对象调用save方法时，会自动调用序列化器类中的update方法
        2、update方法用于对数据进行更新操作
        3、序列化器类中的update方法，instance参数为待更新的模型对象，validated _data参数为校验通过之后的数据（一般字典类型)
        4、在调用save方法时，可以传递任意的关键字参数，并且会自动合并到validated_data字典中
        5、update方法一般需要将更新成功之后模型对象返回
        """
        req_ser.save()
        """
        project_d = Projects.objects.get(id=pk)
        project_d.name = req_ser.validated_data.get("name")
        project_d.leader = req_ser.validated_data.get("leader")
        project_d.is_execute = req_ser.validated_data.get("is_execute")
        project_d.save()
        """
        """序列化输出
        serializer = ProjectSerializer(instance=project_d)
        """
        return JsonResponse(req_ser.data, status=201)

    """删除项目信息"""

    def delete(self, request, pk):
        Projects.objects.get(id=pk).delete()
        return JsonResponse({"删除项目信息": f"{pk}"}, status=204)


def sql(request):
    """创建方式一"""
    # obj = Projects(name="java项目", leader="curry")
    # obj.save()
    """创建方式二"""
    # obj = Projects.objects.create(name="HTML项目", leader="FFF")
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
    """id__gt大于、id__gte大于等于"""
    # obj = Projects.objects.filter(id__gte=3)
    """id__in"""
    # obj = Projects.objects.filter(id__in=[1, 2, 5])
    """name__contains包含、name__icontains忽略大小写"""
    # obj = Projects.objects.filter(name__icontains="c")
    """
    name__istartswith以某某某开头
    name__iendswith以某某某结尾
    name__iregex正则
    """
    # obj = Projects.objects.filter(name__iendswith="项目")
    """exclude为反向查询"""
    # obj = Projects.objects.exclude(name__iendswith="项目")

    """创建从表数据"""
    # project_obj = Projects.objects.get(name="Vue项目")
    """方式一"""
    # interfaces_obj = Interfaces.objects.create(name="Vue项目-删除接口", tester="curry", projects=project_obj)
    """方式二"""
    # interfaces_obj = Interfaces.objects.create(name="java项目-注册接口", tester="curry", projects_id=project_obj.id)

    """查询从表获取父表数据"""
    # obj = Interfaces.objects.filter(name__contains="登录").first().projects
    # obj = Interfaces.objects.filter(projects__name="java项目")
    # obj = Interfaces.objects.filter(projects__leader__contains="cu")
    """查询父表获取从表数据"""
    # obj = Projects.objects.filter(inter__name="java项目-注册接口").first().leader
    # obj = Projects.objects.filter(leader__contains="cu")[1].inter.all()

    """or"""
    # obj = Projects.objects.filter(Q(name__contains="py") | Q(leader__contains="F")).values()

    """and"""
    """方式一"""
    # obj = Projects.objects.filter(name__contains="py", leader__contains="x")
    """方式二"""
    # obj = Projects.objects.filter(name__contains="py").filter(leader__contains="cu")

    """排序"""
    # obj = Projects.objects.filter(Q(name__contains="py") | Q(leader__contains="F")).order_by("name")  # 升序
    # obj = Projects.objects.filter(Q(name__contains="py") | Q(leader__contains="F")).order_by("-name")  # 降序
    # obj = Projects.objects.filter(Q(name__contains="py") | Q(leader__contains="F")).order_by("name, leader")  # 多条件

    """更新"""
    # 方式一 (update_fields=["name"]指定更新字段, 默认全更新)
    # project_obj = Projects.objects.get(id=1)
    # project_obj.name = "python中级项目"
    # project_obj.save(update_fields=["name"])

    # 方式二
    # obj = Projects.objects.filter(leader="curry").update(leader="sc")

    """删除"""
    # 方式一
    # obj = Projects.objects.get(name="JS项目").delete()

    # 方式二
    # obj = Projects.objects.filter(leader="sc").delete()
    """聚合运算"""
    # sum=Count("id") 返回自定义字段名
    # obj = Projects.objects.filter(leader__contains="x").aggregate(sum=Count("id"))

    """分组"""
    # obj = Projects.objects.values("id").annotate(inter=Count("inter"))
    obj = "null"
    return JsonResponse({"msg": f"{obj}"})
