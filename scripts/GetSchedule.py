import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
try:
    from scripts.Objects import *
except:
    from Objects import *

def getGames(date):
    log = open("log.txt", "w")
    
    year, month, day = date.split('-')
    url = "https://www.sports-reference.com/cbb/boxscores/index.cgi?month=" + month + "&day=" + day + "&year=" + year
    page = requests.get(url)
    scoreboard = BeautifulSoup(page.content, 'html.parser')
    schedule = scoreboard.find('div', id = 'games')
    games = scoreboard.find_all('table', class_='teams')
    allObjects = []
    regex = "/cbb/schools/(.*)/"
    for game in games:
        teams = game.find_all('a')
        awayTag = teams[0]
        homeTag = teams[1]
        try:
            homeLink = homeTag['href']
            search = re.search(regex, homeLink)
            home = Team(homeTag.get_text(), search.group(1))
        except:
            home = Team(homeTag.get_text(), homeTag.get_text().replace(' ', '-').lower())
        try:
            awayLink = awayTag['href']
            search = re.search(regex, awayLink)
            away = Team(awayTag.get_text(), search.group(1))
        except:
            away = Team(awayTag.get_text(), awayTag.get_text().replace(' ', '-').lower())

        for ch in ['\'', '(', ')']:
            if ch in home.name: home.name = home.name.replace(ch, '')
            if ch in away.name: away.name = away.name.replace(ch, '')

        allObjects.append(
            Game(
                date,
                home,
                away
            )
        )
    log.close()
    return allObjects