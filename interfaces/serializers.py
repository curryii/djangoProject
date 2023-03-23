from rest_framework import serializers
from projects.models import Projects


class InterfaceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    tester = serializers.CharField()

    """从表获取父表信息"""
    projects = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())
