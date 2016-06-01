#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#


import psycopg2


def connect(database_name="tournament"):
    try:
        conn = psycopg2.connect("dbname={}".format(database_name))
        c = conn.cursor()
        return conn, c
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""

    conn, c = connect()
    SQL = "DELETE FROM matches;"
    c.execute(SQL)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn, c = connect()
    SQL = "DELETE FROM players;"
    c.execute(SQL)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn, c = connect()
    SQL = "SELECT * FROM players;"
    c.execute(SQL)
    rowcount = c.rowcount
    return rowcount
    conn.close()


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    conn, c = connect()
    SQL = "INSERT INTO players (name) VALUES (%s);"
    data = (name,)
    c.execute(SQL, data)
    conn.commit()
    conn.close()


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

    conn, c = connect()
    SQL = "SELECT id, name, wins, matchesplayed FROM standings ORDER BY wins;"
    c.execute(SQL)
    return c.fetchall()
    conn.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn, c = connect()
    SQL = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    data = (winner, loser)
    c.execute(SQL, data)
    conn.commit()
    conn.close()


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

    conn, c = connect()

    # --------Match pairing procedure--------
    # Create an iteration counter by dividing our table record row count by two.
    # This lets us know how many pairs we need to make.
    SQL = "SELECT * from players;"
    c.execute(SQL)
    iter = c.rowcount / 2

    # Sort on wins to give our table some consistency. We could create pairs
    # in any direction after this sort.
    SQL = "SELECT id, name from wins_counter ORDER BY wins;"
    c.execute(SQL)

    # We iterate based on the counter, add the resulting tuples together,
    # append, and return our list.
    pairings = []
    while iter != 0:
        tup = c.fetchone() + c.fetchone()
        pairings.append( tup )
        iter = iter - 1
    return pairings
