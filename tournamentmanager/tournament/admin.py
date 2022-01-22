from django.contrib import admin
from django.contrib.admin import site
import adminactions.actions as actions

from .models import Game, Tournament, Team, Score, Match
actions.add_to_site(site)

admin.site.register(Game)
admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Score)
admin.site.register(Match)
