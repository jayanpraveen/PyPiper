# Generated by Django 3.2 on 2021-04-25 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0007_alter_upload_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload',
            name='title',
        ),
    ]