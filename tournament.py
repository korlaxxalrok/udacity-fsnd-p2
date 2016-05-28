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

    conn = connect()
    c = conn.cursor()

    c.execute("DELETE FROM matches")

    # We also need to touch up other match data from table 'players'.
    # Reset wins, losses, and matches in table 'players':
    c.execute("UPDATE players SET wins = 0")
    c.execute("UPDATE players SET losses = 0")
    c.execute("UPDATE players SET matches = 0")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM players")
    rowcount = c.rowcount
    return rowcount


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
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

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, name, wins, matches from players ORDER BY wins")
    return c.fetchall()
    conn.commit()
    conn.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()

    # Insert winner/loser into table 'matches'.
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser))

    # Update winner/loser in table 'players'.
    c.execute("UPDATE players SET wins = wins + 1 WHERE id = %s", (winner,))
    c.execute("UPDATE players SET losses = losses + 1 WHERE id = %s", (loser,))

    # Update matches in table 'players'.
    c.execute("UPDATE players SET matches = wins + losses WHERE id =%s", (winner,))
    c.execute("UPDATE players SET matches = wins + losses WHERE id =%s", (loser,))
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

    conn = connect()
    c = conn.cursor()

    # INFO:
    #
    # Create an iteration counter by dividing our row count by two. This lets
    # us iterate correctly so that we can create a new pair each iteration.
    #
    # Sort on wins to give our table some consistency. We could create pairs
    # in any direction after this sort.
    #
    # We iterate, add the resulting tuples together, and then append
    # and return our list.

    #1) Create iter variable.
    c.execute("SELECT * from players")
    iter = c.rowcount / 2

    #2) Sort on wins.
    c.execute("SELECT id, name from players ORDER BY wins")

    #3) Iterate, create pairing tuples, and append to our list.
    pairings = []
    while iter != 0:
        tup = c.fetchone() + c.fetchone()
        pairings.append( tup )
        iter = iter - 1
    return pairings
