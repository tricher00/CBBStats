from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import Team
from .models import Player
from .models import GameLine
from .models import Conference
from scripts.SQLFunctions import getPlayerLineById
from scripts.GetSchedule import getGames
import pandas as pd

def home(request):
    today = datetime.now()
    date = "{}-{}-{}".format(today.year, '%02d' % today.month, '%02d' % today.day)
    return render(request, 'home.html', {'games': getGames(date)})

def school_page(request, school):
    team = Team.objects.get(name=school)
    players = Player.objects.filter(team_id=team.id)
    stats = [PlayerStats(x) for x in players]
    return render(request, 'school.html', {'team': team, 'players': stats})
    
def player_page(request, player_id):
    player = Player.objects.get(id=player_id)
    stats = PlayerStats(player)
    lines = GameLine.objects.filter(player_id=player.id)
    return render(request, 'player.html', {'player': player, 'stats': stats, 'lines': lines})
    
def conference_page(request, conference):
    conf = Conference.objects.get(abbrv=conference)
    teams = Team.objects.filter(conference=conf.abbrv).order_by('-conf_wins', '-wins')
    return render(request, 'conference.html', {'conference': conf, 'teams': teams})
    
class PlayerStats:
    def __init__(self, player):
        playerLine = getPlayerLineById(player.id)
        self.name = player.name
        self.id = player.id
        self.lines = GameLine.objects.filter(player_id=player.id)
        self.MPG = round(playerLine.MPG, 2)
        self.PPG = round(playerLine.PPG, 2)
        self.RPG = round(playerLine.RPG, 2)
        self.APG = round(playerLine.APG, 2)
        self.SPG = round(playerLine.SPG, 2)
        self.BPG = round(playerLine.BPG, 2)
        if playerLine['FG%'] is None:
            self.FGP = 0.0
        else:
            self.FGP = round(playerLine['FG%'], 3)
        if playerLine['3P%'] is None:
            self.TPP = 0.0
        else:
            self.TPP = round(playerLine['3P%'], 3)
        if playerLine['FT%'] is None:
            self.FTP = 0.0
        else:
            self.FTP = round(playerLine['FT%'], 3)
        
