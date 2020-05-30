from django.contrib import admin

from music_collection.compilations.models import Release, Series, Track


class TrackInlineAdmin(admin.TabularInline):
    extra = 0
    model = Track
    ordering = ("order_index",)


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("name", "year")
    inlines = (TrackInlineAdmin,)
    fieldsets = (
        (None, {"fields": ("series", "name", "slug", "year", "discogs_release_id")}),
        ("Important dates", {"fields": ("created_at", "last_checked_at",
                                        "updated_at")})
    )
    readonly_fields = ("created_at", "last_checked_at", "updated_at")


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("name",)
