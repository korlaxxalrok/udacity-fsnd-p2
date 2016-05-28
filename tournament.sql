-- Table definitions for the tournament project.

-- Clean up everything so we can create from scratch.
-- This throws an error if the DB does not exist but proceeds with creation.
DROP DATABASE tournament;

-- Create DB.
CREATE DATABASE tournament;

-- Connect to DB 'tournament'.
\c tournament

-- Create table 'players'.
CREATE TABLE players (id serial NOT NULL PRIMARY KEY, name text NOT NULL, wins int default 0, losses int default 0, matches int default 0);

-- Create table 'matches'.
CREATE TABLE matches (match_id serial NOT NULL PRIMARY KEY, winner int NOT NULL, loser int NOT NULL);
