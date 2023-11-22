# Generated by Django 3.2.22 on 2023-11-22 16:38

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50, verbose_name='First Name')),
                ('lname', models.CharField(max_length=50, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('phone', models.CharField(max_length=20, verbose_name='Contact Number')),
                ('msg', models.TextField(verbose_name='Message')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='MusicMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=100)),
                ('song_title', models.CharField(max_length=100)),
                ('song_file', cloudinary.models.CloudinaryField(max_length=255, verbose_name='song_file')),
                ('song_image', cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dsqr7dgjt/image/upload/v1700499377/jnepz9qayczlbb0gqvao.png', max_length=255, verbose_name='song_image')),
            ],
            options={
                'verbose_name': 'Music',
                'verbose_name_plural': 'Music',
            },
        ),
        migrations.CreateModel(
            name='CommentMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('dislikes', models.ManyToManyField(related_name='comment_dis_likes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='musicapp.musicmod')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='profiles.userprofile')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.userprofile')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
