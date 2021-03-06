# Generated by Django 2.2.12 on 2020-05-30 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compilations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='discogs_release_id',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='release',
            name='last_checked_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
