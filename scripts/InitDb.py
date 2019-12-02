import mysql.connector as sql

def main():
    db = "CBBStats"

    conn = sql.connect(user='root', password='password', host='127.0.0.1')    
    c = conn.cursor()       

    c.execute(
        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db)
    )

    conn.close() 
    conn = sql.connect(user='root', password='password', host='127.0.0.1', database=db)    
    c = conn.cursor()

    c.execute(
        "CREATE TABLE game_line(id INTEGER PRIMARY KEY AUTO_INCREMENT, game_id INTEGER, date DATE, season INTEGER, player_id VARCHAR(50), team_id VARCHAR(50), opponent_id VARCHAR(50), location VARCHAR(50), minutes INTEGER, fg_made INTEGER, fg_attempt INTEGER, two_made INTEGER, two_attempt INTEGER, three_made INTEGER, three_attempt INTEGER, ft_made INTEGER, ft_attempt INTEGER, orb INTEGER, drb INTEGER, trb INTEGER, ast INTEGER, stl INTEGER, blk INTEGER, tov INTEGER, pf INTEGER, pts INTEGER, coolness INTEGER);"
    )
    print("Created game_line table")
    c.execute(
        "CREATE TABLE team(id VARCHAR(50) PRIMARY KEY, name VARCHAR(50));"
    )
    print("Created team table")
    c.execute(
        "CREATE TABLE conference(abbrv VARCHAR(50) PRIMARY KEY, name VARCHAR(50));"
    )
    print("Created conference table")
    c.execute(
        "CREATE TABLE player(id VARCHAR(50) PRIMARY KEY, name VARCHAR(50));"
    )
    print("Created player table")
    c.execute(
        "CREATE TABLE game(id INTEGER PRIMARY KEY AUTO_INCREMENT, date DATE, season INTEGER, conf_game INTEGER, home_id VARCHAR(50), away_id VARCHAR(50), home_score INTEGER, away_score INTEGER);"
    )
    print("Created game table")

if __name__ == "__main__": main()
