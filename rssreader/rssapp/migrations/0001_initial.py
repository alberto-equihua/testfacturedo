# Generated by Django 2.2.7 on 2020-08-07 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_id', models.CharField(default='', max_length=200)),
                ('link', models.CharField(default='', max_length=200)),
                ('published', models.DateTimeField()),
                ('summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(default='', max_length=100)),
                ('title', models.CharField(default='', max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RssChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('url', models.CharField(default='', max_length=200)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rssapp.Category')),
                ('entries_ids', models.ManyToManyField(to='rssapp.Entry')),
                ('feed_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rssapp.Feed')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(default='', max_length=10)),
                ('password', models.CharField(default='', max_length=10)),
                ('is_admin', models.BooleanField()),
                ('channels_ids', models.ManyToManyField(to='rssapp.RssChannel')),
            ],
        ),
    ]