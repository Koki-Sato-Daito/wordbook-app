# Generated by Django 3.2 on 2021-09-25 17:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wordname', models.CharField(max_length=128, unique=True, verbose_name='単語')),
                ('meaning', models.CharField(max_length=128, verbose_name='意味')),
                ('pos', models.CharField(max_length=128, verbose_name='品詞')),
                ('python_freq', models.IntegerField(blank=True, verbose_name='出現回数(python)')),
                ('mistake_user', models.ManyToManyField(related_name='users', related_query_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'vocabulary',
            },
        ),
    ]