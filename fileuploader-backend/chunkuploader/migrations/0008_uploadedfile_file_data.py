# Generated by Django 5.1.1 on 2024-09-15 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chunkuploader', '0007_remove_uploadedfile_file_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='file_data',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
