# Generated by Django 2.2 on 2019-10-15 14:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0007_auto_20191014_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('image', models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图')),
                ('url', models.URLField(verbose_name='访问地址')),
                ('index', models.IntegerField(default=100, verbose_name='顺序')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
            },
        ),
    ]
