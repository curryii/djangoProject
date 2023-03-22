from rest_framework import serializers


class InterfaceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    tester = serializers.CharField()


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
                                 })
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
