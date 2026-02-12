from django.db import migrations, models
from django.core.validators import RegexValidator
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AppClient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="软删除标志")),
                ("created_time", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_time", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="全局唯一标识")),
                ("app_id", models.CharField(max_length=100, unique=True, validators=[RegexValidator(message="应用标识只能包含字母、数字、下划线和连字符", regex="^[a-zA-Z0-9_-]+$")], verbose_name="应用标识")),
                ("app_name", models.CharField(max_length=200, verbose_name="应用名称")),
                ("key_id", models.CharField(max_length=64, unique=True, verbose_name="Key ID")),
                ("secret_hash", models.CharField(max_length=256, verbose_name="密钥哈希")),
                ("allowed_ips", models.TextField(blank=True, default="", verbose_name="允许访问的IP")),
                ("scopes", models.TextField(blank=True, default="", verbose_name="权限范围")),
                ("status", models.CharField(choices=[("active", "启用"), ("inactive", "禁用")], default="active", max_length=10, verbose_name="状态")),
            ],
            options={
                "verbose_name": "应用客户端",
                "verbose_name_plural": "应用客户端",
                "db_table": "djs_integration_app_client",
                "ordering": ["-id"],
            },
        ),
        migrations.AddIndex(
            model_name="appclient",
            index=models.Index(fields=["app_id"], name="djs_integra_app_id_2a59d1_idx"),
        ),
        migrations.AddIndex(
            model_name="appclient",
            index=models.Index(fields=["key_id"], name="djs_integra_key_id_996d8c_idx"),
        ),
        migrations.AddIndex(
            model_name="appclient",
            index=models.Index(fields=["status"], name="djs_integra_status_e7b71f_idx"),
        ),
        migrations.AddIndex(
            model_name="appclient",
            index=models.Index(fields=["created_time"], name="djs_integra_created__fae62f_idx"),
        ),
    ]
