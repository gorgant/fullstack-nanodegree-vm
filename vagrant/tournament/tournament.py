#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    sql = """UPDATE playerStandings SET wins = 0, matches = 0;"""
    db = connect()
    c = db.cursor()
    c.execute(sql)
    db.commit()
    db.close()



def deletePlayers():
    """Remove all the player records from the database."""
    clear_players = """DELETE FROM players;"""
    db = connect()
    c = db.cursor()
    c.execute(clear_players)
    db.commit()
    db.close()

    clear_standings = """DELETE FROM playerStandings;"""
    db = connect()
    c = db.cursor()
    c.execute(clear_standings)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    sql = """SELECT COUNT(name) FROM players;"""
    db = connect()
    c = db.cursor()
    c.execute(sql)
    data = c.fetchone()
    count = data[0]
    db.commit()
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    add_to_players = """INSERT INTO players(name) VALUES (%s) RETURNING playerId;"""


    db = connect()
    c = db.cursor()
    c.execute(add_to_players,(name,))
    player_id = c.fetchone()[0]
    db.commit()
    db.close()

    add_to_playerStandings = """INSERT INTO playerStandings(playerId, name, wins, matches) VALUES (%s, %s, %s, %s);"""
    wins = 0
    matches = 0

    db = connect()
    c = db.cursor()
    c.execute(add_to_playerStandings,(player_id, name, wins, matches,))
    db.commit()
    db.close()




def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    fetch_player_standings = """SELECT * FROM playerStandings ORDER BY wins;"""
    db = connect()
    c = db.cursor()
    c.execute(fetch_player_standings)
    player_standings_list = c.fetchall()
    db.commit()
    db.close()
    return player_standings_list



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    update_winner = """UPDATE playerStandings SET wins = wins + 1, matches = matches + 1 WHERE playerId = (%s);"""
    db = connect()
    c = db.cursor()
    c.execute(update_winner,(winner,))
    db.commit()
    db.close()

    update_loser = """UPDATE playerStandings SET matches = matches + 1 WHERE playerId = (%s);"""
    db = connect()
    c = db.cursor()
    c.execute(update_loser,(loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    clear_pairings = """DELETE FROM swissPairings;"""
    db = connect()
    c = db.cursor()
    c.execute(clear_pairings)
    db.commit()
    db.close()
    # GREG: Fetch a list of players, then parse that list in pairs of two
    fetch_player_list = """SELECT playerId, name FROM playerStandings ORDER BY wins;"""
    db = connect()
    c = db.cursor()
    c.execute(fetch_player_list)
    player_list_length = c.rowcount
    counter = player_list_length
    while (counter > 0):
        player_list = c.fetchmany(2)
        #GREG: converts the player list, which has two tuples of two, into a flat list of 1 tuple w/ 4 values
        #see https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
        match_up = [i for sub in player_list for i in sub]
        player1Id = match_up[0]
        player1Name = match_up[1]
        player2Id = match_up[2]
        player2Name = match_up[3]
        add_to_swissPairings = """INSERT INTO swissPairings(player1Id, player1Name, player2Id, player2Name)
                                VALUES (%s, %s, %s, %s);"""
        db2 = connect()
        c2 = db2.cursor()
        c2.execute(add_to_swissPairings,(player1Id, player1Name, player2Id, player2Name,))
        db2.commit()
        db2.close()
        counter -= 2
    db.commit()
    db.close()

    fetch_swissPairings_list = """SELECT * FROM swissPairings;"""
    db = connect()
    c = db.cursor()
    c.execute(fetch_swissPairings_list)
    swissPairings_list = c.fetchall()
    db.commit()
    db.close()
    return swissPairings_list




