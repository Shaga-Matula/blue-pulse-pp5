# Generated by Django 3.2.22 on 2024-01-11 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0002_alter_musicmod_song_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicmod',
            name='song_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='musicmod',
            name='song_image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='song_image'),
        ),
    ]
