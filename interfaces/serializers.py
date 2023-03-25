from rest_framework import serializers
from projects.models import Projects
from interfaces.models import Interfaces


class InterfaceSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="接口id",
                                  help_text="接口id",
                                  read_only=True)
    name = serializers.CharField(label="接口名称",
                                 help_text="接口名称")
    tester = serializers.CharField(label="接口负责人",
                                   help_text="接口负责人")
    projects_id = serializers.IntegerField()

    """从表获取父表信息"""
    projects = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        interfaces_obj = Interfaces.objects.create(**validated_data)
        return interfaces_obj

    def update(self, instance, validated_data):
        pass
