# Generated by Django 2.2.5 on 2019-09-25 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('em_website', '0002_post_test1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='test1',
        ),
    ]