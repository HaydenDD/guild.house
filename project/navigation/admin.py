from django.contrib import admin
from models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem


class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]

admin.site.register(Menu, MenuAdmin)
