# Generated by Django 2.2.11 on 2020-03-04 22:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Series',
                'verbose_name_plural': 'Series',
            },
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2099)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='compilations.Series'))
            ],
            options={
                'unique_together': {('series', 'slug')},
                'verbose_name': 'Release',
                'verbose_name_plural': 'Releases',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_index', models.PositiveIntegerField()),
                ('position', models.CharField(max_length=10)),
                ('artist', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=250)),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='compilations.Release')),
            ],
            options={
                'unique_together': {('release', 'order_index')},
                'verbose_name': 'Track',
                'verbose_name_plural': 'Tracks',
            },
        ),
    ]
