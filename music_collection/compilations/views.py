from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from music_collection.compilations.models import Release, Series


class SeriesListView(ListView):
    model = Series
    ordering = ("name",)


class ReleaseBaseView(object):
    model = Release

    @cached_property
    def series(self):
        return get_object_or_404(Series, slug=self.kwargs["series"])

    def get_context_data(self, **kwargs):
        context = super(ReleaseBaseView, self).get_context_data(**kwargs)
        context["series"] = self.series
        return context

    def get_queryset(self):
        queryset = super(ReleaseBaseView, self).get_queryset()
        return queryset.filter(series=self.series)


class ReleaseListView(ReleaseBaseView, ListView):
    ordering = ("order_index",)


class ReleaseDetailView(ReleaseBaseView, DetailView):
    slug_url_kwarg = "release"
