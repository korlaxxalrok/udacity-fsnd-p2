-- Table definitions for the tournament project.

-- Clean up everything so we can create from scratch.
-- This throws an error if the DB does not exist but proceeds with creation.
DROP DATABASE IF EXISTS tournament;

-- Create DB.
CREATE DATABASE tournament;

-- Connect to DB 'tournament'.
\c tournament

-- Create table 'players'.
CREATE TABLE players (
  id serial NOT NULL PRIMARY KEY,
  name text NOT NULL
);

-- Create table 'matches'.
CREATE TABLE matches (
  match_id serial NOT NULL PRIMARY KEY,
  winner serial NOT NULL REFERENCES players(id),
  loser serial NOT NULL REFERENCES players(id)
);

-- Create wins_counter view
-- This view joins the 'players' and 'matches' tables to count the number of
-- wins by the player(s).
CREATE VIEW wins_counter
AS
  SELECT players.id,
         players.name,
         COUNT(matches.winner) AS wins
  FROM   players
         LEFT JOIN matches
                ON players.id = matches.winner
  GROUP  BY players.id;

-- Create match_counter view
-- This view joins the 'players' and 'matches' tables to cunt the number of
-- matches played by the player(s).
CREATE VIEW match_counter
AS
  SELECT players.id,
         players.name,
         COUNT(matches) AS matchesplayed
  FROM   players
         LEFT JOIN matches
                ON players.id = matches.winner
                    OR players.id = matches.loser
  GROUP  BY players.id;

-- Create standings view
-- This view joins the wins_count and match_count views to display overall
-- player standings information. We can also use this view to help with creating
-- new pairings.
CREATE VIEW standings
AS
  SELECT wins_counter.id,
         wins_counter.name,
         wins_counter.wins,
         match_counter.matchesplayed
  FROM   wins_counter
         JOIN match_counter
           ON wins_counter.id = match_counter.id
 ORDER BY wins DESC;
