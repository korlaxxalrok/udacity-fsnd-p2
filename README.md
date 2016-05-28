# Udacity Full Stack Web Developer Nanodegree
## Project 2: Tournament results

### Info
This project deals with Python, PostgreSQL, and Psycopg. We used these tools to create some functionality around running a [Swiss-system tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament). I've come across this style of tournament before and I like it a lot. Everyone gets to play and the better players still get to progress as expected (and generally a winner gets to do winner-type stuff at the end).

### How you might use this
There are several potentially useful functions defined in 'tournament.py'. A possible use case might be to take a look at those functions and use them to build a DIY tournament tool. They could be extended as appropriate. As it stands, this project isn't probably super useful out of the box.

#### Functions contained in 'tournament.py'

connect - Meant to connect to the database.

deleteMatches - Remove all the matches records from the database.

deletePlayers - Remove all the player records from the database.

countPlayers - Returns the number of players currently registered

registerPlayer - Adds a player to the tournament database.

playerStandings - Returns a list of the players and their win records, sorted by wins. You can use the player standings table created in your .sql file for reference.

reportMatch - This is to simply populate the matches table and record the winner and loser as (winner,loser) in the insert statement.

swissPairings - Returns a list of pairs of players for the next round of a match. Here all we are doing is the pairing of alternate players from the player standings table, zipping them up and appending them to a list with values:
(id1, name1, id2, name2)

(Most of these are taken verbatim from the Udacity project notes)

### Prerequisites
* Platform:
  * OS X and probably Linux. I have not checked on Windows.
* Python 2.7.x.
  * Probably safest as I haven't checked or tested outside of this.
* Psycopg needs:
  * Python 2 versions from 2.5 to 2.7
  * Python 3 versions from 3.1 to 3.4
  * PostgreSQL versions from 7.4 to 9.4
    * You will need a working PostgreSQL install and we will assume that you can interact with the system in such a way that you can create and delete databases and tables.

### Install and run
* Clone the repo
* 'cd' into the repo directory
* To configure the DB:
  * Run a 'psql' terminal
  * Run '\i tournament.sql' to create the DB and tables
* To use the Python functions:
  * You can test them all out by running Python interactively (shell or IDLE (not tested)) and doing 'import * from tournament'. Do something with them, see if they work :)
  * There is a test script that could, at the very least, help you verify that you have DB access configured as well as the attendant Python files in the right place/you are working out of the right place.
