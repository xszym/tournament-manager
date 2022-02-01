from django.contrib import admin
from django.contrib.admin import site
import adminactions.actions as actions

from .models import Game, TeamJoinRequest, Tournament, Team, Match, TeamTournamentRequest
actions.add_to_site(site)

admin.site.register(Game)
admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(TeamTournamentRequest)
admin.site.register(TeamJoinRequest)
