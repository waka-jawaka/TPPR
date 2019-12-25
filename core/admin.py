from django.contrib import admin

from .models import Alternative, Criterion, Mark, Person, Result, Vector


def normalize_all_marks(modeladmin, request, queryset):
	for mark in queryset:
		mark.normalize()
normalize_all_marks.short_description = 'Нормализировать выбранные оценки'


class MarkAdmin(admin.ModelAdmin):
	actions = [normalize_all_marks,]
	list_filter = ['criterion__name',]
	list_display = ['__str__', 'rate']
	readonly_fields = ('other_rates',)
	fields = ['criterion', 'name', 'rate', 'number', 'normalized', 'other_rates']

	def other_rates(self, obj):
		return ", ".join([str(x.rate) for x in Mark.objects.filter(criterion=obj.criterion)])


admin.site.register(Alternative)
admin.site.register(Criterion)
admin.site.register(Mark, MarkAdmin)
admin.site.register(Person)
admin.site.register(Result)
admin.site.register(Vector)
