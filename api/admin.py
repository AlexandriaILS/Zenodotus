from django.contrib import admin
from reversion.admin import VersionAdmin

from api.models import ItemType, Record, Subject


@admin.register(Record)
class RecordAdmin(VersionAdmin):
    pass


@admin.register(ItemType)
class ItemTypeAdmin(VersionAdmin):
    pass


# admin.site.register(Record, RecordAdmin)
# admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Subject)
