from django.contrib import admin

from music_collection.compilations.models import Release, Series, Track


class TrackInlineAdmin(admin.TabularInline):
    extra = 0
    model = Track
    ordering = ("order_index",)


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("name", "year")
    list_filter = ("series",)
    inlines = (TrackInlineAdmin,)
    fieldsets = (
        (None, {
            "fields": (
                "series", "order_index", "name", "slug", "year",
                "discogs_release_id"
            )
        }),
        ("Important dates", {
            "fields": ("created_at", "last_checked_at", "updated_at")
        })
    )
    ordering = ("series__name", "order_index",)
    readonly_fields = ("created_at", "last_checked_at", "updated_at")
    sortable_by = ()


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("name", "num_releases")
    ordering = ("name",)

    def num_releases(self, obj):
        return obj.releases.count()
