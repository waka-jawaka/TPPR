from django.contrib import admin

from .models import Alternative, Criterion, Mark, Person, Result


def normalize_all_marks(modeladmin, request, queryset):
	for mark in queryset:
		mark.normalize()
normalize_all_marks.short_description = 'Нормализировать выбранные оценки'


class MarkAdmin(admin.ModelAdmin):
	actions = [normalize_all_marks]


admin.site.register(Alternative)
admin.site.register(Criterion)
admin.site.register(Mark, MarkAdmin)
admin.site.register(Person)
admin.site.register(Result)
