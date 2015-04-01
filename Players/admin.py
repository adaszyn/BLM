from django.contrib import admin

from Players.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    view_on_site = True
    list_display = ('pk', 'first_name', 'last_name', 'number', 'team', 'position', 'age', 'height', 'weight')
    list_filter = ['team', 'position']
    search_fields = ['first_name', 'last_name']

    # Disable delete when team has 5 players
    def has_delete_permission(self, request, obj=None):
        try:
            return False if Player.objects.filter(team=obj.team).count() == 5 else True
        except AttributeError:
            pass

    # Disable delete action form the list; not ideal, disables delete for all players
    def get_actions(self, request):
        actions = super(PlayerAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions