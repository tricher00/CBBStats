class Game:
    def __init__(self, date, home, away):
        self.date = date
        self.home = home
        self.home.isHome = True
        self.away = away
        self.link = None
        self.homeScore = 0
        self.awayScore = 0
        year, month, day = date.split('-')
        if int(month) > 6:
            self.season = int(year) + 1
        else:
            self.season = int(year)
        
class Team:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.isHome = False
        self.box = None