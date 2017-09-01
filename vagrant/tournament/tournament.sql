-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- This table stores the player names and their respective IDs
CREATE TABLE players ( playerId SERIAL,
                      name TEXT );

-- This table stores player rankings
CREATE TABLE playerStandings ( playerId INTEGER,
                              name TEXT,
                              wins INTEGER,
                              matches INTEGER );

-- This table stores the matchups between the players (may need to be tweaked)
CREATE TABLE swissPairings ( player1Id INTEGER,
                            player1Name TEXT,
                            player2Id INTEGER,
                            player2Name TEXT );


