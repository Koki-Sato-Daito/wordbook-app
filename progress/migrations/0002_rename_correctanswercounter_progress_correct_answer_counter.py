# Generated by Django 3.2 on 2022-05-17 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='progress',
            old_name='correctAnswerCounter',
            new_name='correct_answer_counter',
        ),
    ]