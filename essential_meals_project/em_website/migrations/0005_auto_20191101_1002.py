# Generated by Django 2.2.5 on 2019-11-01 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('em_website', '0004_category_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(help_text='One ingredient per line', verbose_name='Indigrents'),
        ),
    ]
