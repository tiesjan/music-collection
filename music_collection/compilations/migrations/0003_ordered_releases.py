# Generated by Django 2.2.12 on 2020-06-05 18:34

from django.db import migrations, models


def fill_release_order_index(apps, schema_editor):
    Release = apps.get_model("compilations", "Release")
    Series = apps.get_model("compilations", "Series")

    for series in Series.objects.order_by("pk"):
        releases = Release.objects.filter(series=series).order_by("created_at")
        for i, release in enumerate(releases):
            release.order_index = i
            release.save(update_fields=["order_index"])


class Migration(migrations.Migration):

    dependencies = [
        ('compilations', '0002_automatic_updates'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='order_index',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),

        migrations.RunPython(fill_release_order_index, migrations.RunPython.noop),

        migrations.AlterField(
            model_name='release',
            name='order_index',
            field=models.PositiveIntegerField(),
        ),
    ]
