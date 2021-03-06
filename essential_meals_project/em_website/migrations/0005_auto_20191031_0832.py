# Generated by Django 2.2.5 on 2019-10-31 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('em_website', '0004_category_recipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(help_text='One ingredient per line', verbose_name='Indigrents'),
        ),
    ]
