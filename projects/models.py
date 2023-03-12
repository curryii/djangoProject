from django.db import models
from utils.base_model import BaseModel


# Create your models here.

class Projects(BaseModel):
    name = models.CharField(verbose_name="项目名称", help_text="项目名称", unique=True, max_length=50)
    leader = models.CharField(verbose_name="项目负责人", help_text="项目负责人", max_length=10)
    is_execute = models.BooleanField(verbose_name="是否启动项目", help_text="是否启动项目", default=True)
    desc = models.TextField(verbose_name="项目描述信息", help_text="项目描述信息", null=True, blank=True, default="")

    class Meta:
        """指定创建数据库表名称"""
        db_table = 'tb_projects'
        """数据库表描述"""
        verbose_name = "项目表"
        verbose_name_plural = "项目表"
        """排序"""
        ordering = ["id"]

    def __str__(self):
        return f"Projects({self.name})"
