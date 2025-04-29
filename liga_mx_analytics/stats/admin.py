from django.contrib import admin

# Register your models here.
from .models import Teams, Fixtures, AllPlayers, FieldPlayerStats, TeamStats, GoalkeepersStats, Referees, Stadiums

admin.site.register(Teams)
admin.site.register(Fixtures)
admin.site.register(AllPlayers)
admin.site.register(FieldPlayerStats)
admin.site.register(TeamStats)
admin.site.register(GoalkeepersStats)
admin.site.register(Referees)
admin.site.register(Stadiums)
