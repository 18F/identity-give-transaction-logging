# Generated by Django 3.1.5 on 2021-03-19 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_auto_20210319_1640"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transactionrecord",
            name="csp",
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name="transactionrecord",
            name="provider",
            field=models.CharField(max_length=16),
        ),
    ]
