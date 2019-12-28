from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import Team
from .models import Player
from .models import Game
from .models import GameLine
from .models import Conference
from scripts.GetSchedule import getGames
from scripts.ViewsUtils import *

def home(request):
    today = datetime.now()
    date = "{}-{}-{}".format(today.year, '%02d' % today.month, '%02d' % today.day)
    return render(request, 'home.html', {'games': getGames(date)})

def school_page(request, school):
    team = Team.objects.get(id=school)
    conference, conference_id = GetConferenceData(school, 2020)
    games = Game.objects.filter(Q(home_id = school) | Q(away_id = school))
    seasons = sorted(list(set([x.season for x in games])))
    records = list()
    for season in seasons:
        records.append(GetRecord(school, games, season))
    return render(request, 'school.html', {
        'team': team,
        'conference': conference,
        'conference_id': conference_id,
        'colors': SchoolColors(school),
        'records': records
    })

def school_season_page(request, school, season):
    team = Team.objects.get(id=school)
    conference, conference_id = GetConferenceData(school, season)
    lines = GameLine.objects.filter(team_id=school, season=season)
    playerIds = set([x.player_id for x in lines])
    playerStats = list()
    for id in playerIds:
        player = Player.objects.get(id=id)
        playerStats.append(PlayerStatsSeason(player, season))
    return render(request, 'school-season.html', {
        'team': team,
        'conference': conference,
        'conference_id': conference_id,
        'colors': SchoolColors(school),
        'player_stats': playerStats
    })

def player_page(request, player_id):
    player = Player.objects.get(id=player_id)
    lines = GameLine.objects.filter(player_id=player.id)
    careerStats = PlayerStatsCareer(player)
    seasons = sorted(list(set([x.season for x in lines])))
    seasonStats = list()
    for season in seasons:
        seasonStats.append(PlayerStatsSeason(player, season))
    return render(request, 'player.html', {
        'player': player, 'careerStats': careerStats, 'seasonStats': seasonStats, 'lines': lines})
    
def conference_page(request, conference):
    conf = Conference.objects.get(abbrv=conference)
    teams = Team.objects.filter(conference=conf.abbrv).order_by('-conf_wins', '-wins')
    return render(request, 'conference.html', {'conference': conf, 'teams': teams})      
