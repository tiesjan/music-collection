from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Series(models.Model):
    name = models.CharField(
        max_length=50
    )

    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"


class Release(models.Model):
    order_index = models.PositiveIntegerField()

    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name="releases"
    )

    name = models.CharField(
        max_length=50
    )

    slug = models.SlugField()

    year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2099)]
    )

    discogs_release_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        unique=True
    )

    last_checked_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def ordered_tracks(self):
        return self.tracks.order_by("order_index")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("series", "slug")

        verbose_name = "Release"
        verbose_name_plural = "Releases"


class Track(models.Model):
    release = models.ForeignKey(
        Release,
        on_delete=models.CASCADE,
        related_name="tracks"
    )

    order_index = models.PositiveIntegerField()

    position = models.CharField(
        max_length=10
    )

    artist = models.CharField(
        max_length=250
    )

    title = models.CharField(
        max_length=250
    )

    def __str__(self):
        return "{}. {} - {}".format(self.position, self.artist, self.title)

    class Meta:
        unique_together = (
            ("release", "order_index"),
        )

        verbose_name = "Track"
        verbose_name_plural = "Tracks"
