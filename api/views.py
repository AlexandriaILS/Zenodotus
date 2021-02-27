from django.shortcuts import render
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (
    BibliographicLevelSerializer,
    ItemTypeSerializer,
    ItemTypeBaseSerializer,
    SubjectSerializer,
    RecordSerializer,
)
from api.models import BibliographicLevel, ItemType, ItemTypeBase, Subject, Record


def index(request):
    return render(request, "index.html")


class RecordViewSet(ModelViewSet):
    serializer_class = RecordSerializer
    basename = "record"

    def get_queryset(self):
        queryset = Record.objects.all()
        modifiers = Q()
        # localhost:8000/api/record/?title=stuff&authors=guy
        if title := self.request.query_params.get("title"):
            modifiers.add(
                (Q(title__iexact=title) | Q(subtitle__iexact=title)),
                modifiers.connector,
            )

        if authors := self.request.query_params.get("authors"):
            modifiers.add((Q(authors__iexact=authors)), modifiers.connector)

        if itemtype := self.request.query_params.get("type_id"):
            if itemtype == 2:
                breakpoint()
            modifiers.add((Q(type__id=itemtype)), modifiers.connector)

        if len(modifiers) > 0:
            queryset = queryset.filter(modifiers)

        return queryset


class ItemTypeBaseViewSet(ReadOnlyModelViewSet):
    serializer_class = ItemTypeBaseSerializer
    basename = "itemtypebase"
    queryset = ItemTypeBase.objects.all()


class ItemTypeViewSet(ModelViewSet):
    serializer_class = ItemTypeSerializer
    basename = "itemtype"

    def get_queryset(self):
        queryset = ItemType.objects.all()
        if searchterm := self.request.query_params.get("q"):
            queryset = queryset.filter(name=searchterm)

        return queryset


class SubjectViewSet(ModelViewSet):
    serializer_class = SubjectSerializer
    basename = "subject"

    def get_queryset(self):
        queryset = Subject.objects.all()
        if searchterm := self.request.query_params.get("q"):
            queryset = queryset.filter(name=searchterm)

        return queryset


class BibliographicLevelViewSet(ModelViewSet):
    serializer_class = BibliographicLevelSerializer
    basename = "bibliographiclevel"
    queryset = BibliographicLevel.objects.all()
