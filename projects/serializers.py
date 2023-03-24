from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from projects.models import Projects

"""
1、可以在序列化器字段上使用validators指定自定义的校验规则
2、 validators必须得为序列类型（列表），在列表中可以添加多个校验规则
3、DRF框架自带UniqueValidator校验器，必须得使用queryset指定查询集对象，用于对该字段进行校验
4、UniqueValidator校验器，可以使用message指定自定义报错信息
5、校验规则的执行顺序?

对字段类型进行校验 -> 依次验证validators列表中的校验规则 -> 从右到左依次验证其他规 -> 调用单字段校验方法
-> to_internal_value调用结束 -> 调用多字段联合校验方法validate方法

1、可以在类外自定义校验函数
2、第一个参数为待校验的值
3、如果校验不通过，必须得抛出serializers.ValidationError('报错信息')异常，同时可以指定具体的报错信息
4、需要将校验函数名放置到validators列表中

1、可以在序列化器类中对单个字段进行校验
2、单字段的校验方法名称，必须把validate_作为前缀，加上待校验的字段名，如: validate_待校验的字段名
3、如果校验不通过，必须得返回serializers.ValidationError('具体报错信息’)异常
4、如果校验通过，往往需要将校验之后的值返回
5、如果该字段在定义时添加的校验规则不通过，那么是不会调用单字段的校验方法

1、可以在序列化器类中对多个字段进行联合校验
2、使用固定的validate方法，会接收上面校验通过之后的字典数据
3、当所有字段定义时添加的校验规则都通过,且每个字典的单字段校验方法通过的情况下，才会调用validate

1、to_internal_value方法，是所有字段开始进行校验时入口方法（最先调用的方法)
2、会依次对序列化器类的各个序列化器字段进行校验
3、应用场景：对各个单字段校验结束之后的数据进行修改

1、to representation方法，是所有字段开始进行序列化输出时的入口方法（最先调用的方法)
"""


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
        user = validated_data.pop("user")
        age = validated_data.pop("age")
        project_obj = Projects.objects.create(**validated_data)
        return project_obj

    def update(self, instance, validated_data: dict):
        instance.name = validated_data.get("name") or instance.name
        instance.leader = validated_data.get("leader") or instance.leader
        instance.is_execute = validated_data.get("is_execute") or instance.is_execute
        instance.save()
        return instance
