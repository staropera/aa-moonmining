# Generated by Django 3.1.6 on 2021-03-31 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("moonmining", "0007_notification_details"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="text",
        ),
    ]
