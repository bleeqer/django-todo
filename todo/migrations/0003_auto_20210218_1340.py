# Generated by Django 3.1.6 on 2021-02-18 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20210218_1336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='createdtime',
            new_name='created',
        ),
    ]
