# Generated by Django 5.1.1 on 2024-09-15 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chunkuploader', '0006_uploadedfile_file_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedfile',
            name='file_data',
        ),
    ]
