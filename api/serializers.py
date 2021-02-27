from rest_framework.serializers import ModelSerializer, SerializerMethodField
from reversion.models import Version

from api.models import ItemType, ItemTypeBase, Record, Subject, BibliographicLevel

from api.taggit_serializer import (
    TaggitSerializer,
    TagListSerializerField,
)


class RecordSerializer(TaggitSerializer, ModelSerializer):
    tags = TagListSerializerField(required=False)
    revision_id = SerializerMethodField("get_revision_id")

    def get_revision_id(self, obj):
        try:
            return max(
                [item.revision_id for item in Version.objects.get_for_object(obj)]
            )
        except ValueError:
            return 0

    class Meta:
        model = Record
        fields = (
            "id",
            "title",
            "authors",
            "subtitle",
            "uniform_title",
            "notes",
            "series",
            "subjects",
            "tags",
            "image",
            "type",
            "bibliographic_level",
            "revision_id",
        )


class ItemTypeSerializer(ModelSerializer):
    class Meta:
        model = ItemType
        fields = ("id", "name", "base")


class BibliographicLevelSerializer(ModelSerializer):

    name = SerializerMethodField(read_only=True)

    def get_name(self, obj):
        # obj is model instance
        return obj.get_name_display()

    class Meta:
        model = ItemType
        fields = ("id", "name")


class ItemTypeBaseSerializer(ModelSerializer):
    name = SerializerMethodField(read_only=True)

    def get_name(self, obj):
        # obj is model instance
        return obj.get_name_display()

    class Meta:
        model = ItemTypeBase
        fields = ("id", "name")


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name")
