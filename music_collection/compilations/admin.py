from django.contrib import admin

from music_collection.compilations.models import Release, Series, Track


class TrackInlineAdmin(admin.TabularInline):
    model = Track
    ordering = ("position",)


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("name", "year")
    inlines = (TrackInlineAdmin,)


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("name",)
