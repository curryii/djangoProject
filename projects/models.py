from django.db import models


# Create your models here.

class Projects(models.Model):
    ids = models.IntegerField(verbose_name="项目主键", help_text="项目主键", primary_key=True)
    name = models.CharField(verbose_name="项目名称", help_text="项目名称", unique=True, max_length=50)
    leader = models.CharField(verbose_name="项目负责人", help_text="项目负责人", max_length=10)
    is_execute = models.BooleanField(verbose_name="是否启动项目", help_text="是否启动项目", default=True)
    desc = models.TextField(verbose_name="项目描述信息", help_text="项目描述信息", null=True, blank=True, default="")
    create_time = models.DateTimeField(verbose_name="创建时间", help_text="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="修改时间", help_text="修改时间", auto_now=True)

    class Meta:
        db_table = 'tb_projects'
