from django.db import models
from projects.models import Projects
from utils.base_model import BaseModel


# Create your models here.


class Interfaces(BaseModel):
    name = models.CharField(verbose_name="接口名称", help_text="接口名称", unique=True, max_length=20)
    tester = models.CharField(verbose_name="测试人员", help_text="测试人员", max_length=10)

    """建立外键字段"""
    projects = models.ForeignKey(Projects, on_delete=models.CASCADE, verbose_name="所属项目", help_text="所属项目",
                                 related_name="inter")

    class Meta:
        """指定创建数据库表名称"""
        db_table = 'tb_interfaces'
        """数据库表描述"""
        verbose_name = "接口表"
        verbose_name_plural = "接口表"
        """排序"""
        ordering = ["id"]

    def __str__(self):
        return f"Interfaces({self.name})"
