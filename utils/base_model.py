from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(verbose_name="ID主键", help_text="ID主键", primary_key=True)
    create_time = models.DateTimeField(verbose_name="创建时间", help_text="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="修改时间", help_text="修改时间", auto_now=True)

    class Meta:
        """抽象模型类在迁移不会创建表"""
        abstract = True
