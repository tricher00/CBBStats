import string
import os
from shutil import copyfile
import mysql.connector as sql
import pandas as pd
try:
    from scripts.Objects import Game
except:
    from Objects import Game

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = "CBBStats"

def connectToDb():
    return sql.connect(user='root', password='password', host='127.0.0.1', database=DB_NAME)

def getTeamId(teamName):
    conn = connectToDb()
    c = conn.cursor()

    var = (teamName,)
    
    c.execute("SELECT id FROM team WHERE name = %s", var)
    
    temp = c.fetchone()
    return temp[0]

def getTeamConf(teamId, season):
    schoolToConf = pd.read_csv(
        os.path.join(BASE_DIR, "static/ConferenceData/{}_SchoolToConferenceMap.csv".format(season)))
    abbrvs = pd.read_csv(
        os.path.join(BASE_DIR, "static/ConferenceData/{}_ConferenceAbbreviations.csv".format(season)))
    try:
        conf = schoolToConf[schoolToConf.School == teamId].iloc[0].Conference
        abbrv = abbrvs[abbrvs.Conference == conf].iloc[0].Abbreviation
        return abbrv
    except:
        return 'none'
    
def getPlayerId(playerName, team = None):
    conn = connectToDb()
    c = conn.cursor()
        
    if team == None:
        var = (playerName,)
        c.execute("SELECT team.name FROM player INNER JOIN team ON player.team_id = team.id WHERE player.name = %s COLLATE NOCASE", var)
        temp = c.fetchall()
        print(temp)
        if len(temp) > 1:
            print("There are multiple players with the name {} which one would you like".format(playerName))
            teams = [x[0] for x in temp]
            for y in teams:
                print("- {}".format(y))
            team = raw_input()
            team = team.lower()
            team = team.replace(' ', '-')
            while team not in teams:
                print("Please enter a valid team name")
                team = raw_input()
                team = team.lower()
                team = team.replace(' ', '-')
        elif len(temp) == 1:
            team = temp[0][0]
        else:
            print("No Player with that name")
            return
        
    teamId = getTeamId(team)
    var = (playerName, teamId)
    c.execute("SELECT id FROM player WHERE name = %s AND team_id = %s COLLATE NOCASE", var)
    temp = c.fetchone()
        
    if temp == None:
        print("No Player with that name")
    conn.close()
    return temp[0]

def insertPlayer(id, player):
    conn = connectToDb()
    conn.text_factory = str
    c = conn.cursor()
    var = (id,)
    c.execute("SELECT * FROM player WHERE id = %s", var)
    temp = c.fetchone()

    if temp == None:
        var = (id, player)
        c.execute("INSERT INTO player (id, name) VALUES (%s,%s)", var)
        conn.commit()

    conn.close()

def AddTeamsToDb(teams):
    conn = connectToDb()
    c = conn.cursor()
    for team in teams:
        var = (team.name,)
        
        c.execute("SELECT id FROM team WHERE name = %s", var)
        
        temp = c.fetchone()
        
        if temp == None:
            var = (team.id, team.name)
            c.execute("INSERT INTO team (id, name) VALUES (%s,%s)", var)
            conn.commit()
    conn.close()

def insertGameLine(line, gameId, season):
    conn = connectToDb()
    c = conn.cursor()
    
    date, team, opponent, location, player, id, mins, fg_made, fg_attempt, two_made, two_attempt, three_made, three_attempt, ft_made, ft_attempt, orb, drb, trb, ast, stl, blk, tov, pf, pts, coolness = line
    
    teamId = getTeamId(team)
    opponentId = getTeamId(opponent)
    insertPlayer(id, player)
    
    var = (gameId, date, season, id, teamId, opponentId, location, mins, fg_made, fg_attempt, two_made, two_attempt, three_made, three_attempt, ft_made, ft_attempt, orb, drb, trb, ast, stl, blk, tov, pf, pts, coolness)
    
    c.execute("INSERT INTO game_line (game_id, date, season, player_id, team_id, opponent_id, location, minutes, fg_made, fg_attempt, two_made, two_attempt, three_made, three_attempt, ft_made, ft_attempt, orb, drb, trb, ast, stl, blk, tov, pf, pts, coolness) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", var)
    conn.commit()
    conn.close()

def insertGame(game):
    conn = connectToDb()
    c = conn.cursor()

    isConf = 0
    date = game.date

    homeId = game.home.id
    homeScore = game.homeScore
    homeConf = getTeamConf(homeId, game.season)

    awayId = game.away.id
    awayScore = game.awayScore
    awayConf = getTeamConf(awayId, game.season)

    if homeConf == awayConf: isConf = 1

    var = (isConf, date, game.season, homeId, awayId, homeScore, awayScore)

    c.execute("INSERT INTO game (conf_game, date, season, home_id, away_id, home_score, away_score) VALUES (%s,%s,%s,%s,%s,%s,%s)", var)
    conn.commit()

    var = (date, homeId, awayId)

    c.execute("SELECT id FROM game WHERE date = %s AND home_id = %s AND away_id = %s", var)
    temp = c.fetchone()

    conn.close()

    return temp[0]
    
def getPlayerLine(playerName):
    conn = connectToDb()
    c = conn.cursor()

    playerName = string.capwords(playerName)
    
    playerId = getPlayerId(playerName)
    
    var = (playerId,)
    
    queryList = [
        "SELECT player.name as Player, ",
        "team.name as School, "
        "CAST(Count(*) as float) as Games, ",
        "SUM(minutes) / CAST(Count(*) as float) as MPG, ",
        "SUM(pts) / CAST(Count(*) as float) as PPG, ",
        "SUM(ast) / CAST(Count(*) as float) as APG, ",
        "SUM(orb) / CAST(Count(*) as float) as ORPG, ",
        "SUM(drb) / CAST(Count(*) as float) as DRPG, ",
        "SUM(trb) / CAST(Count(*) as float) as RPG, ",
        "SUM(stl) / CAST(Count(*) as float) as SPG, ",
        "SUM(blk) / CAST(Count(*) as float) as BPG, ",
        "SUM(tov) / CAST(Count(*) as float) as TPG, ",
        "SUM(coolness) / CAST(Count(*) as float) as CPG, ",
        "SUM(fg_made) / CAST(SUM(fg_attempt) as float) as 'FG%', ",
        "SUM(two_made) / CAST(SUM(two_attempt) as float) as '2P%', ",
        "SUM(three_made) / CAST(SUM(three_attempt) as float) as '3P%', ",
        "SUM(ft_made) / CAST(SUM(ft_attempt) as float) as 'FT%', ",
        "SUM(pts) as Points, ",
        "SUM(ast) as Asists, ",
        "SUM(orb) as ORB, ",
        "SUM(drb) as DRB, ",
        "SUM(trb) as TRB, ",
        "SUM(coolness) as Coolness ",
        "FROM game_line ",
        "INNER JOIN team ON team.id = game_line.team_id ",
        "INNER JOIN player ON player.id = game_line.player_id WHERE player.id = %s "
    ]
    
    query = ""
    
    for x in queryList: query += x
    
    c.execute(query, var)
    temp = c.fetchone()
    
    colNames = ['Player', 'School', 'Games', 'MPG', 'PPG', 'APG', 'ORPG', 'DRPG', 'RPG', 'SPG', 'BPG', 'TPG', 'CPG', 'FG%', '2P%', '3P%', 'FT%', 'Points', 'Assists', 'ORB', 'DRB', 'TRB', 'Coolness']
    
    conn.close()
    
    return pd.Series(temp, colNames)

def getPlayerLineById(playerId):
    conn = connectToDb()
    c = conn.cursor()

    var = (playerId,)
    
    queryList = [
        "SELECT player.name as Player, ",
        "team.name as School, "
        "CAST(Count(*) as float) as Games, ",
        "SUM(minutes) / CAST(Count(*) as float) as MPG, ",
        "SUM(pts) / CAST(Count(*) as float) as PPG, ",
        "SUM(ast) / CAST(Count(*) as float) as APG, ",
        "SUM(orb) / CAST(Count(*) as float) as ORPG, ",
        "SUM(drb) / CAST(Count(*) as float) as DRPG, ",
        "SUM(trb) / CAST(Count(*) as float) as RPG, ",
        "SUM(stl) / CAST(Count(*) as float) as SPG, ",
        "SUM(blk) / CAST(Count(*) as float) as BPG, ",
        "SUM(tov) / CAST(Count(*) as float) as TPG, ",
        "SUM(coolness) / CAST(Count(*) as float) as CPG, ",
        "SUM(fg_made) / CAST(SUM(fg_attempt) as float) as 'FG%', ",
        "SUM(two_made) / CAST(SUM(two_attempt) as float) as '2P%', ",
        "SUM(three_made) / CAST(SUM(three_attempt) as float) as '3P%', ",
        "SUM(ft_made) / CAST(SUM(ft_attempt) as float) as 'FT%', ",
        "SUM(pts) as Points, ",
        "SUM(ast) as Asists, ",
        "SUM(orb) as ORB, ",
        "SUM(drb) as DRB, ",
        "SUM(trb) as TRB, ",
        "SUM(coolness) as Coolness ",
        "FROM game_line ",
        "INNER JOIN team ON team.id = game_line.team_id ",
        "INNER JOIN player ON player.id = game_line.player_id WHERE player.id = %s "
    ]
    
    query = ""
    
    for x in queryList: query += x
    
    c.execute(query, var)
    temp = c.fetchone()
    
    colNames = ['Player', 'School', 'Games', 'MPG', 'PPG', 'APG', 'ORPG', 'DRPG', 'RPG', 'SPG', 'BPG', 'TPG', 'CPG', 'FG%', '2P%', '3P%', 'FT%', 'Points', 'Assists', 'ORB', 'DRB', 'TRB', 'Coolness']
    
    conn.close()
    
    return pd.Series(temp, colNames)
    
def getAllPlayerLines():
    conn = connectToDb()
    c = conn.cursor()
    
    queryList = [
        "SELECT player.id as Id, ",
        "player.name as Player, ",
        "team.name as School, "
        "CAST(Count(*) as float) as Games, ",
        "SUM(minutes) / CAST(Count(*) as float) as MPG, ",
        "SUM(pts) / CAST(Count(*) as float) as PPG, ",
        "SUM(ast) / CAST(Count(*) as float) as APG, ",
        "SUM(orb) / CAST(Count(*) as float) as ORPG, ",
        "SUM(drb) / CAST(Count(*) as float) as DRPG, ",
        "SUM(trb) / CAST(Count(*) as float) as RPG, ",
        "SUM(stl) / CAST(Count(*) as float) as SPG, ",
        "SUM(blk) / CAST(Count(*) as float) as BPG, ",
        "SUM(tov) / CAST(Count(*) as float) as TPG, ",
        "SUM(coolness) / CAST(Count(*) as float) as CPG, ",
        "SUM(fg_made) / CAST(SUM(fg_attempt) as float) as 'FG%', ",
        "SUM(two_made) / CAST(SUM(two_attempt) as float) as '2P%', ",
        "SUM(three_made) / CAST(SUM(three_attempt) as float) as '3P%', ",
        "SUM(ft_made) / CAST(SUM(ft_attempt) as float) as 'FT%', ",
        "SUM(pts) / (2 * (CAST(SUM(fg_attempt) as float) + (.44 * SUM(ft_attempt)))) as 'TS%', ",
        "SUM(pts) as Points, ",
        "SUM(ast) as Asists, ",
        "SUM(orb) as ORB, ",
        "SUM(drb) as DRB, ",
        "SUM(trb) as TRB, ",
        "SUM(coolness) as Coolness ",
        "FROM game_line ",
        "INNER JOIN player ON player.id = game_line.player_id ",
        "INNER JOIN team ON team.id = game_line.team_id ",
        "GROUP BY player_id;"
    ]
    
    query = ""
    
    for x in queryList: query += x
    
    c.execute(query)
    temp = c.fetchall()
    
    colNames = ['Id', 'Player', 'School', 'Games', 'MPG', 'PPG', 'APG', 'ORPG', 'DRPG', 'RPG', 'SPG', 'BPG', 'TPG', 'CPG', 'FG%', '2P%', '3P%', 'FT%', 'TS%', 'Points', 'Asists', 'ORB', 'DRB', 'TRB', 'Coolness']
    df = pd.DataFrame(temp)
    df.columns = colNames
    conn.close()
    players = df['Id'].tolist()
    sos = []
    for player in players:
        print(player)
        sos.append(getSOS(player))
    df['SOS'] = sos
    return df

def getSOS(playerId):
    conn = connectToDb()
    c = conn.cursor()

    var = (playerId,)

    query = "SELECT opponent_id FROM game_line WHERE player_id = (%s);"

    c.execute(query, var)
    temp = c.fetchall()

    oppIds = [x[0] for x in temp]

    sumSos = 0
    for id in oppIds:
        newVar = (id,)
        newQuery = "SELECT wins/CAST((wins + losses) AS float)  FROM team WHERE id = (%s);"
        c.execute(newQuery, newVar)
        sos = c.fetchone()[0]
        try:
            sumSos += sos
        except:
            continue

    return float(sumSos/len(oppIds))
    
def getSimplePlayerLine(playerName):
    conn = connectToDb()
    c = conn.cursor()
    
    playerName = string.capwords(playerName)
    
    playerId = getPlayerId(playerName)

    var = (playerId,)
    
    queryList = [
        "SELECT player.name as Player, ",
        "team.name as School, ",
        "CAST(Count(*) as float) as Games, ",
        "SUM(minutes) / CAST(Count(*) as float) as MPG, ",
        "SUM(pts) / CAST(Count(*) as float) as PPG, ",
        "SUM(ast) / CAST(Count(*) as float) as APG, ",
        "SUM(trb) / CAST(Count(*) as float) as RPG, ",
        "SUM(stl) / CAST(Count(*) as float) as SPG, ",
        "SUM(blk) / CAST(Count(*) as float) as BPG, ",
        "SUM(tov) / CAST(Count(*) as float) as TPG, ",
        "SUM(fg_made) / CAST(SUM(fg_attempt) as float) as 'FG%', ",
        "SUM(two_made) / CAST(SUM(two_attempt) as float) as '2P%', ",
        "SUM(three_made) / CAST(SUM(three_attempt) as float) as '3P%', ",
        "SUM(ft_made) / CAST(SUM(ft_attempt) as float) as 'FT%' ",
        "FROM game_line ",
        "INNER JOIN team ON team.id = player.team_id ",
        "INNER JOIN player ON player.id = game_line.player_id  WHERE player.id = %s ",
        "COLLATE NOCASE;"
    ]
    
    query = ""
    
    for x in queryList: query += x
    
    c.execute(query, var)
    temp = c.fetchone()
    
    colNames = ['Player', 'School', 'Games', 'MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TPG', 'FG%', '2P%', '3P%', 'FT%']
    
    conn.close()
    
    return pd.Series(temp, colNames)
    
    
def getTeamPage(teamName):
    conn = connectToDb()
    c = conn.cursor()
    
    teamName = teamName.lower()
    teamName = teamName.replace(' ', '-')
    
    colNames = ['Player', 'Games', 'MPG', 'PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TPG', 'CPG', 'FG%', '2P%', '3P%', 'FT%', 'FGA', 'FGM', '2PA', '2PM', '3PA', '3PM', 'FTA', 'FTM']
    
    var = (teamName, )
    
    queryList = [
        "SELECT player.name as Player, ",
        "CAST(Count(*) as float) as Games, ",
        "SUM(minutes) / CAST(Count(*) as float) as MPG, ",
        "SUM(pts) / CAST(Count(*) as float) as PPG, ",
        "SUM(ast) / CAST(Count(*) as float) as APG, ",
        "SUM(trb) / CAST(Count(*) as float) as RPG, ",
        "SUM(stl) / CAST(Count(*) as float) as SPG, ",
        "SUM(blk) / CAST(Count(*) as float) as BPG, ",
        "SUM(tov) / CAST(Count(*) as float) as TPG, ",
        "SUM(coolness) / CAST(Count(*) as float) as CPG, "
        "SUM(fg_made) / CAST(SUM(fg_attempt) as float) as 'FG%', ",
        "SUM(two_made) / CAST(SUM(two_attempt) as float) as '2P%', ",
        "SUM(three_made) / CAST(SUM(three_attempt) as float) as '3P%', ",
        "SUM(ft_made) / CAST(SUM(ft_attempt) as float) as 'FT%', ",
        "SUM(fg_attempt), ",
        "SUM(fg_made), ",
        "SUM(two_attempt), ",
        "SUM(two_made), ",
        "SUM(three_attempt), ",
        "SUM(three_made), ",
        "SUM(ft_attempt), ",
        "SUM(ft_made) ",
        "FROM game_line ",
        "INNER JOIN team ON team.id = player.team_id ",
        "INNER JOIN player ON player.id = game_line.player_id WHERE team.name = %s "
        "GROUP BY player_id;"
    ]
    
    query = ""
    
    for x in queryList: query += x
    
    c.execute(query , var)

    temp = c.fetchall()
    
    page = pd.DataFrame(temp, columns = colNames)
     
    conn.close()    
        
    return page.round(2)

def getLeaderboard(stat, limit):
    conn = connectToDb()
    c = conn.cursor()
    
    statQuery = {
        "Coolness" : "SUM(coolness)",
        "Points" : "SUM(pts)",
        "Asists" : "SUM(ast)",
        "Rebounds" : "SUM(trb)",
        "Offensive Rebounds" : "SUM(orb)",
        "Defensive Rebounds" : "SUM(drb)",
        "Steals" : "SUM(stl)",
        "CPG" : "SUM(coolness)/Cast(COUNT(*) as float)",
        "PPG" : "SUM(pts)/Cast(COUNT(*) as float)",
        "APG" : "SUM(ast)/Cast(COUNT(*) as float)",
        "RPG" : "SUM(trb)/Cast(COUNT(*) as float)",
        "ORPG" : "SUM(orb)/Cast(COUNT(*) as float)",
        "DRPG" : "SUM(drb)/Cast(COUNT(*) as float)",
        "SPG" : "SUM(stl)/Cast(COUNT(*) as float)"
    }
        
    var = (limit, )
    
    query = ""
    
    queryList = [
        "SELECT player.name as Player, ",
        "team.name as Team, "
        "CASE WHEN CAST(Count(*) as float) >= 5 THEN {} END as stat ".format(statQuery[stat]),
        "FROM game_line ",
        "INNER JOIN player ON player.id = game_line.player_id ",
        "INNER JOIN team ON team.id = game_line.team_id ",
        "GROUP BY player_id ",
        "ORDER by stat DESC ",
        "LIMIT %s;"
    ]
        
    for x in queryList: query += x
    
    c.execute(query, var)
    
    result = c.fetchall()
    
    players = [x[0] for x in result]
    teams = [string.capwords(x[1].replace('-',' ')) for x in result]
    stats = [x[2] for x in result]
    
    df = pd.DataFrame(
        {
            'Player': players,
            'Team': teams,
            stat: stats
        }
    )
    
    df = df[[u'Player', u'Team', stat]]
    
    df.index = df.index + 1
    
    conn.close()
    
    return df.round(2)
    
def getWatchability():
    conn = connectToDb()
    c = conn.cursor()
    c.execute("SELECT team.name, team_id, SUM(minutes), SUM(coolness) FROM game_line INNER JOIN team on team_id = team.id GROUP BY team_id")
    temp = c.fetchall()
    
    df = pd.DataFrame(temp, columns=["team", "id", "minutes", "coolness"])
    
    watch = []
    for index, row in df.iterrows():
        if row.coolness == 0 or row.minutes == 0:
            watch.append(0)
        else:
            watch.append(float(row.coolness)/row.minutes)
    
    normed = [0.0] * len(watch)
    mean = sum(watch)/len(watch)
    
    for i in range(len(watch)):
        inc = watch[i] - mean
        normed[i] = inc/mean * 100
        
    watchFrame = pd.DataFrame({'Team':df.team.values, 'Watchability':normed})
    watchFrame = watchFrame.sort_values(by='Watchability', ascending=False)
    
    conn.close()
    return watchFrame

def getMaxDate():
    conn = connectToDb()
    c = conn.cursor()
    c.execute("SELECT max(date) FROM game_line;")
    date = c.fetchone()[0]
    if date == None: return "The database is empty"
    else: return date
    