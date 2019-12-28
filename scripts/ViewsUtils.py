import os
import pandas as pd
from scripts.SQLFunctions import getPlayerLineById, getPlayerLineSeasonById

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#TODO: Add this to db
class SchoolColors:
    def __init__(self, schoolName):
        if "-am-" in schoolName or schoolName.endswith("-am"):
            schoolName = schoolName.replace("-am", "-a&m")
        if "-at-" in schoolName or schoolName.endswith("-at"):
            schoolName = schoolName.replace("-at", "-a&t")
        schoolName = schoolName.title()
        colors = pd.read_csv(os.path.join(BASE_DIR, "static/colors.csv"))
        school = colors[colors.School == schoolName]
        if len(school) == 0:
            self.Primary = "#FFFFFF"
            self.Secondary = "#000000"
        elif school.isnull().values.any():
            self.Primary = "#FFFFFF"
            self.Secondary = "#000000"
        else:
            self.Primary = school.Primary.item()
            self.Secondary = school.Secondary.item()

class PlayerStatsSeason:
    def __init__(self, player, season):
        playerLine = getPlayerLineSeasonById(player.id, season)
        self.season = season
        self.name = player.name
        self.id = player.id
        self.school = playerLine.School
        self.school_id = playerLine.School_Id
        self.games = int(playerLine.Games)
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

class PlayerStatsCareer:
    def __init__(self, player):
        playerLine = getPlayerLineById(player.id)
        self.name = player.name
        self.id = player.id
        self.games = int(playerLine.Games)
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

class Record:
    def __init__(self, season, wins, losses, confWins, confLosses):
        self.season = season
        self.wins = wins
        self.losses = losses
        self.confWins = confWins
        self.confLosses = confLosses

def GetConferenceData(school, year):
    schoolToConf = pd.read_csv(os.path.join(
        BASE_DIR, "static/ConferenceData/{}_SchoolToConferenceMap.csv".format(year)))
    conf = schoolToConf[schoolToConf.School == school].iloc[0].Conference
    abbrvs = pd.read_csv(os.path.join(
        BASE_DIR, "static/ConferenceData/{}_ConferenceAbbreviations.csv".format(year)))
    abbrv = abbrvs[abbrvs.Name == conf].iloc[0].Abbreviation

    return [conf, abbrv]

def GetRecord(school, games, season):
    wins = losses = confWins = confLosses = 0

    homeGames = [x for x in games if x.season == season and x.home_id == school]
    awayGames = [x for x in games if x.season == season and x.away_id == school]

    for game in homeGames:
        if game.home_score > game.away_score:
            wins += 1
            if game.conf_game:
                confWins += 1
        else:
            losses += 1
            if game.conf_game:
                confLosses += 1
    for game in awayGames:
        if game.away_score > game.home_score:
            wins += 1
            if game.conf_game:
                confWins += 1
        else:
            losses += 1
            if game.conf_game:
                confLosses += 1

    return Record(season, wins, losses, confWins, confLosses)
