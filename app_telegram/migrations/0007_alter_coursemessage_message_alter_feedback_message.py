# Generated by Django 4.2.4 on 2023-11-18 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_telegram', '0006_alter_course_options_alter_coursemessage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemessage',
            name='message',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='message',
            field=models.TextField(max_length=5000),
        ),
    ]
