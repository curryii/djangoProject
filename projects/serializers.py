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

    """
    1、如果定义了一个模型类中没有的字段，并且该字段需要输出（序列化输出）
    2、需要在create方法、update方法中的模型对象上，添加动态的属性即可
    """
    token = serializers.CharField(read_only=True)

    """
    3、如果定义了一个模型类中没有的字段，并且该字段需要输入（反序列化输入)
    4、需要在create方法、update方法调用之前，将该字段pop调用
    """
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
    """
    可以模型序列化器类
    1、继承serializers.ModelSerializer类或其子类
    2、需要在Meta内部类中指定model、 fields类属性参数
    3、model指定模型类（需要生成序列化器的模型类)
    4、fields指定模型类中哪些字段需要自动生成序列化器字段
    5、会给id主键、有指定auto_now_add或者auto_now参数的DateTimeField字段,添加read_only=True,仅仅只进行序列化输出
    6、有设置unique=True的模型字段,会自动在validators列表中添加唯一约束校验validators=[<UniqueValidator(queryset=Projects.objects.all())>]
    7、有设置default=True的模型字段，会自动添加required=False
    8、有设置null=True的模型字段，会自动添加allow_null=True
    9、有设置blank=True的模型字段，会自动添加allow_blank=True
    """

    """
    修改自动生成的序列化器字段
    方式一:
    a．可以重新定义模型类中同名的字段
    b.自定义字段的优先级会更高（会覆盖自动生成的序列化器字段)
    
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
    
    inter = InterfaceSerializer(label="项目接口信息", help_text="项目接口信息", read_only=True, many=True)
    token = serializers.CharField(read_only=True)
    """

    class Meta:
        model = Projects
        """
        fields指定模型类中哪些字段需要自动生成序列化器字段
        a.如果指定为"_all_"，那么模型类中所有的字段都需要自动转化为序列化器字段
        fields = ("id", "name", "leader")
        b.可以传递需要转化为序列化器字段的模型字段名元组
        exclude = ("id", "name")
        c.exclude指定模型类中哪些字段不需要转化为序列化器字段
        d.fields元祖中必须指定进行序列化或者反序列化操作的所有字段名称,指定了_all_和exclude除外
        """
        fields = "__all__"

        """
        修改自动生成的序列化器字段
        方式二:
        a.如果自动生成的序列化器字段，只有少量不满足要求，可以在Meta中extra_kwargs字典进行微调
        b.将需要调整的字段作为key，把具体需要修改的内容字典作为value
        """
        extra_kwargs = {
            "leader": {
                "max_length": 20,
                "min_length": 5
            },
            "name": {
                "min_length": 5
            }
        }

        """
        可以将需要批量需要设置read_only=True参数的字段名添加到Meta中read_only_fields元组
        read_only_fields = ("is_execute", "id")
        """
    """
    def create(self, validated_data):
        
        a.继承ModelSerializer之后，ModelSerializer中实现了create和update方法
        b.一般无需再次定义create和update方法
        c.如果父类提供的create和update方法不满足需要时,可以重写create和update方法，最后再调用父类的create和update方法
        
        validated_data.pop("user")
        validated_data.pop("age")
        tmp = super().create(validated_data)
        tmp.token = "001211200"
        return tmp
    """
