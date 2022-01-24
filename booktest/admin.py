from argparse import Action
from dataclasses import field
import imp
from re import search
from django.contrib import admin
from booktest.models import AreaInfo, PicTest
# Register your models here.


class AreaStackedInline(admin.StackedInline):
    model = AreaInfo
    extra = 2


class AreaTabularInline(admin.TabularInline):
    model = AreaInfo
    extra = 2



class AreaInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'atitle', 'title', 'aParent']
    actions_on_bottom = True
    actions_on_top = False
    list_filter = ['atitle']
    search_fields = ['atitle']

    # fields = ['aParent', 'atitle'] 
    fieldsets = (
        ('basic', {'fields': ['atitle']}),
        ('juior', {'fields': ['aParent']})
    )
    inlines = [AreaTabularInline]

admin.site.register(AreaInfo, AreaInfoAdmin)
admin.site.register(PicTest)
