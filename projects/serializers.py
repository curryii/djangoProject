from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from projects.models import Projects


class InterfaceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    tester = serializers.CharField()


def is_contains_keyword(value):
    if "项目" not in value:
        raise serializers.ValidationError("项目名称必须包含项目关键字")


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="项目id",
                                  help_text="项目id",
                                  read_only=True)
    name = serializers.CharField(label="项目名称",
                                 help_text="项目名称",
                                 max_length=20,
                                 min_length=5,
                                 error_messages={
                                     "min_length": "确保包含5个字符",
                                     "max_length": "不超过20个字符"
                                 },
                                 validators=[UniqueValidator(queryset=Projects.objects.all(),
                                                             message="项目名称不能重复"),
                                             is_contains_keyword])
    leader = serializers.CharField(label="项目负责人",
                                   help_text="项目负责人",
                                   default="curry")
    is_execute = serializers.BooleanField(label="是否启动项目",
                                          help_text="是否启动项目",
                                          required=False)
    update_time = serializers.DateTimeField(label="修改时间",
                                            help_text="修改时间",
                                            read_only=True,
                                            format="%Y年%m月%d日 %H:%M:%S")

    # inter = serializers.PrimaryKeyRelatedField(label="项目接口ID",help_text="项目接口ID",read_only=True,many=True)
    # inter = serializers.PrimaryKeyRelatedField(label="项目接口ID", help_text="项目接口ID", many=True,
    # queryset=Interfaces.objects.all())
    # inter = serializers.StringRelatedField(many=True)
    # inter = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    inter = InterfaceSerializer(label="项目接口信息", help_text="项目接口信息", read_only=True, many=True)
    token = serializers.CharField(read_only=True)
    sms_code = serializers.CharField(write_only=True)

    def validate_name(self, attr: str):
        if not attr.endswith("项目"):
            raise serializers.ValidationError("项目名称必须已项目结尾")
        return attr

    def validate_leader(self, attr: str):
        if "pro" not in attr:
            raise serializers.ValidationError("项目负责人必须包含pro")
        return attr

    def validate(self, attrs):
        if "pro" not in attrs.get("name") or not attrs.get("is_execute"):
            raise serializers.ValidationError('"pro" not in attrs.get("name") or not attrs.get("is_execute")')
        return attrs

    def to_internal_value(self, data):
        tmp = super().to_internal_value(data)
        return tmp

    def to_representation(self, instance):
        tmp = super().to_representation(instance)
        return tmp

    def create(self, validated_data):
        validated_data.pop("user")
        validated_data.pop("age")
        validated_data.pop("sms_code")
        project_obj = Projects.objects.create(**validated_data)
        project_obj.token = "token"
        return project_obj

    def update(self, instance, validated_data: dict):
        instance.name = validated_data.get("name") or instance.name
        instance.leader = validated_data.get("leader") or instance.leader
        instance.is_execute = validated_data.get("is_execute") or instance.is_execute
        instance.save()
        return instance


class ProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = "__all__"
        extra_kwargs = {
            "leader": {
                "max_length": 20,
                "min_length": 5
            },
            "name": {
                "min_length": 5
            }

        }
