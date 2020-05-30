from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from music_collection.compilations.models import Release, Track
from music_collection.discogs_api_client import DiscogsAPIClient


class Command(BaseCommand):

    def _get_tracklist(self, release_info):
        tracklist = []
        for item in release_info["tracklist"]:
            # Skip items on tracklist that do not represent an actual track
            if item["type_"] != "track":
                continue

            # Build artist representation
            artist_parts = []
            for artist in item["artists"]:
                artist_parts.append(artist["name"].strip())
                if artist["join"]:
                    artist_parts.append(artist["join"].strip())
            artist = " ".join(artist_parts)

            # Build track info
            track_info = {
                "position": item["position"],
                "artist": artist,
                "title": item["title"]
            }

            # Add track info to tracklist
            tracklist.append(track_info)

        return tracklist

    def handle(self, *args, **options):
        """
        Iterates over all Releases having the field `discogs_release_id` set
        and updates info on the Release from the corresponding Discogs release
        info. The queryset of Releases is ordered by least recently checked.

        First the corresponding Discogs release is retrieved from their API. If
        the Release has never been checked or if the Discogs release has seen
        updates since the last check, the Release info is updated.

        Due to rate limiting in the Discogs API, a hard limit of 50 releases is
        set to be checked.
        """
        api_client = DiscogsAPIClient(settings.DISCOGS_API_ACCESS_TOKEN)

        queryset = Release.objects.exclude(discogs_release_id=None).order_by(
                "last_checked_at", "created_at")
        for release in queryset[:50]:
            # Retrieve Discogs release
            release_info = api_client.get_release(release.discogs_release_id)
            date_changed = datetime.fromisoformat(release_info["date_changed"])

            # Update Release info if needed
            if release.last_checked_at is None or \
                    release.last_checked_at < date_changed:
                # First update info on the related Tracks
                tracklist = self._get_tracklist(release_info)
                existing_tracks = release.ordered_tracks.all()
                num_stored_tracks = release.tracks.count()
                num_retrieved_tracks = len(tracklist)

                # If the number of stored tracks is equal to or greater than
                # the number of tracks retrieved, overwrite existing tracks and
                # delete the remaining ones
                if num_stored_tracks >= num_retrieved_tracks:
                    for i in range(num_stored_tracks):
                        if i < num_retrieved_tracks:
                            existing_tracks[i].position = tracklist[i]["position"]
                            existing_tracks[i].artist = tracklist[i]["artist"]
                            existing_tracks[i].title = tracklist[i]["title"]
                            existing_tracks[i].save()
                        else:
                            existing_tracks[i].delete()

                # If the number of stored tracks is less than the number of
                # tracks retrieved, overwrite existing tracks and add new ones
                else:
                    for i in range(num_retrieved_tracks):
                        if i < num_stored_tracks:
                            existing_tracks[i].position = tracklist[i]["position"]
                            existing_tracks[i].artist = tracklist[i]["artist"]
                            existing_tracks[i].title = tracklist[i]["title"]
                            existing_tracks[i].save()
                        else:
                            Track.objects.create(
                                release=release, order_index=i,
                                position=tracklist[i]["position"],
                                artist=tracklist[i]["artist"],
                                title=tracklist[i]["title"],
                            )

                # Then update info on the Release itself
                release.year = release_info["year"]
                release.save()

            # Mark Release as checked
            release.last_checked_at = timezone.now()
            release.save(update_fields=["last_checked_at"])
