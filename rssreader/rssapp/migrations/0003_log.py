# Generated by Django 2.2.7 on 2020-08-09 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rssapp', '0002_auto_20200807_2258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default='', max_length=200)),
                ('error', models.TextField(default='')),
            ],
        ),
    ]