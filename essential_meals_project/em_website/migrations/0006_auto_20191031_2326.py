# Generated by Django 2.2.5 on 2019-11-01 03:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('em_website', '0005_auto_20191018_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(help_text='One ingredient per line', verbose_name='Ingredients'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='number_of_portions',
            field=models.PositiveIntegerField(default=1, verbose_name='Number of portions'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time_for_preparation',
            field=models.IntegerField(blank=True, default=15, help_text='How many minutes will it take?', null=True, verbose_name='Preparation time'),
        ),
        migrations.CreateModel(
            name='SavedRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Saved Recipe',
                'verbose_name_plural': 'Saved Recipes',
                'ordering': ['name', 'user'],
            },
        ),
    ]
