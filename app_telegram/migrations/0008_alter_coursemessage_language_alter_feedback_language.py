# Generated by Django 4.2.4 on 2023-11-18 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_telegram', '0007_alter_coursemessage_message_alter_feedback_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemessage',
            name='language',
            field=models.CharField(choices=[('en', 'ro')], max_length=2),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='language',
            field=models.CharField(choices=[('en', 'ro')], max_length=2),
        ),
    ]
