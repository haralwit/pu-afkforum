# Generated by Django 2.2 on 2020-03-18 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rating_dislikes',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='post',
            name='rating_likes',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
    ]
