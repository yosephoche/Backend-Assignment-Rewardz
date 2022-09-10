# Generated by Django 4.1.1 on 2022-09-10 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('author', models.CharField(max_length=100, verbose_name='Author')),
                ('publisher', models.CharField(max_length=100, verbose_name='Publisher')),
                ('year', models.CharField(max_length=50, verbose_name='Year')),
                ('description', models.TextField()),
                ('qty', models.IntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
