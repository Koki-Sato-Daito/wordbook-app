# Generated by Django 3.2 on 2022-02-25 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import progress.validations
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('language', models.CharField(max_length=20, validators=[progress.validations.validate_language], verbose_name='言語')),
                ('pos', models.CharField(max_length=20, validators=[progress.validations.validate_pos], verbose_name='品詞')),
                ('mistake', models.BooleanField(verbose_name='不正解')),
                ('index', models.IntegerField(verbose_name='インデックス')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'progress',
            },
        ),
        migrations.AddConstraint(
            model_name='progress',
            constraint=models.UniqueConstraint(fields=('user', 'language', 'pos', 'mistake'), name='progress_unique'),
        ),
    ]
