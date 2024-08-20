from django.contrib import admin

from .models import APRanking, Game, Rivalry, School, Tournament, TournamentRanking

admin.site.register(APRanking)
admin.site.register(Game)
admin.site.register(Rivalry)
admin.site.register(School)
admin.site.register(Tournament)
admin.site.register(TournamentRanking)
