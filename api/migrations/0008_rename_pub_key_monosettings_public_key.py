# Generated by Django 4.2.2 on 2023-07-23 11:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_alter_order_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="monosettings",
            old_name="pub_key",
            new_name="public_key",
        ),
    ]
