from django.db import migrations

from users.constants import EMPLOYEE_GROUP_NAME


def create_employee_group(apps, schema_editor):
    """Создаёт группу сотрудников при применении миграции."""
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name=EMPLOYEE_GROUP_NAME)


def delete_employee_group(apps, schema_editor):
    """Удаляет группу сотрудников при откате миграции."""
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name=EMPLOYEE_GROUP_NAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_employee_group, delete_employee_group),
    ]
