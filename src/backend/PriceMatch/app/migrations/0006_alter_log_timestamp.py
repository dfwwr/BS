# Generated by Django 5.1.4 on 2024-12-25 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_goods_good_platform"),
    ]

    operations = [
        migrations.AlterField(
            model_name="log",
            name="timestamp",
            field=models.DateTimeField(),
        ),
    ]
