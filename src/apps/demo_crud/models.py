from django.db import models
from django_starter_core.db.models import ModelExt


class Item(ModelExt):
    """
    示例商品模型
    """
    name = models.CharField(max_length=100, verbose_name="商品名称")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    description = models.TextField(blank=True, verbose_name="描述")
    is_active = models.BooleanField(default=True, verbose_name="是否上架")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"
        db_table = "demo_item"
        ordering = ["-created_time"]

    def __str__(self):
        return self.name
