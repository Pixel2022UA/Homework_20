# Generated by Django 4.2.2 on 2023-06-29 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name="Author",
        ),
    ]
