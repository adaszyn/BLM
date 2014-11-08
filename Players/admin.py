from django.contrib import admin

from Players.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team', 'position', 'age', 'height', 'weight')
    list_filter = ['team', 'position']
    search_fields = ['first_name', 'last_name']
    view_on_site = True