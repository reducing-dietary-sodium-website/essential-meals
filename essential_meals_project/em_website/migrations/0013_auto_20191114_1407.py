# Generated by Django 2.2.5 on 2019-11-14 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('em_website', '0012_auto_20191110_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='description',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.CharField(max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.CharField(max_length=100, null=True, verbose_name='Name'),
        ),
    ]
