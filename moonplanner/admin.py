from django.contrib import admin

from . import tasks
from .models import Extraction, MiningCorporation, Moon, Refinery


@admin.register(Extraction)
class ExtractionAdmin(admin.ModelAdmin):
    list_display = ("ready_time", "_corporation", "refinery")
    ordering = ("-ready_time",)
    list_filter = (
        "ready_time",
        "refinery__corporation",
        "refinery",
    )
    search_fields = ("refinery__moon__eve_moon__name",)

    actions = ["update_calculated_properties"]

    def update_calculated_properties(self, request, queryset):
        num = 0
        for obj in queryset:
            tasks.update_extraction_calculated_properties.delay(extraction_pk=obj.pk)
            num += 1

        self.message_user(
            request, f"Started updating calculated properties for {num} extractions."
        )

    update_calculated_properties.short_description = (
        "Update calculated properties for selected extrations."
    )

    def _corporation(self, obj):
        return obj.refinery.corporation

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(MiningCorporation)
class MiningCorporationAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "_alliance",
        "character_ownership",
        "is_enabled",
        "last_update_at",
        "last_update_ok",
    )
    ordering = ["eve_corporation"]
    search_fields = ("refinery__moon__eve_moon__name",)
    list_filter = (
        "is_enabled",
        "last_update_ok",
        "eve_corporation__alliance",
    )
    actions = ["update_mining_corporation"]

    def _alliance(self, obj):
        return obj.eve_corporation.alliance

    _alliance.admin_order_field = "eve_corporation__alliance__alliance_name"

    def update_mining_corporation(self, request, queryset):
        for obj in queryset:
            tasks.update_mining_corporation.delay(corporation_pk=obj.pk)
            text = f"Started updating mining corporation: {obj}. "
            self.message_user(request, text)

    update_mining_corporation.short_description = (
        "Update refineres from ESI for selected mining corporations"
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Refinery)
class RefineryAdmin(admin.ModelAdmin):
    list_display = ("name", "moon", "corporation", "eve_type")
    ordering = ["name"]
    list_filter = (
        ("eve_type", admin.RelatedOnlyFieldListFilter),
        "corporation__eve_corporation",
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Moon)
class MoonAdmin(admin.ModelAdmin):
    list_display = ("eve_moon",)

    actions = ["update_calculated_properties"]

    def update_calculated_properties(self, request, queryset):
        num = 0
        for obj in queryset:
            tasks.update_moon_calculated_properties.delay(moon_pk=obj.pk)
            num += 1

        self.message_user(
            request, f"Started updating calculated properties for {num} moons."
        )

    update_calculated_properties.short_description = (
        "Update calculated properties for selected moons."
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
