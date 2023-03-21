from rest_framework import serializers


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="项目id",
                                  help_text="项目id",
                                  read_only=True)
    name = serializers.CharField(label="项目名称",
                                 help_text="项目名称",
                                 max_length=20,
                                 min_length=5)
    leader = serializers.CharField(label="项目负责人",
                                   help_text="项目负责人",
                                   default="curry")
    is_execute = serializers.BooleanField(label="是否启动项目",
                                          help_text="是否启动项目",
                                          required=False)
    update_time = serializers.DateTimeField(label="修改时间",
                                            help_text="修改时间",
                                            read_only=True)
