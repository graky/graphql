# Generated by Django 3.1.4 on 2021-09-15 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("work", "0002_auto_20210915_1317"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recruiter",
            name="closed_vacancies",
            field=models.IntegerField(default=0),
        ),
    ]
