# Generated by Django 2.2.5 on 2019-09-30 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moonplanner', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refinery',
            old_name='location',
            new_name='moon',
        ),
    ]