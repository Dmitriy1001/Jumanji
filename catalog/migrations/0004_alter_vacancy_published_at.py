# Generated by Django 3.2.6 on 2021-09-23 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210923_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='published_at',
            field=models.DateTimeField(verbose_name='Опубликовано'),
        ),
    ]
