DROP TABLE IF EXISTS PlayerStats;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Matches;


CREATE TABLE Matches (
    MatchID varchar(255) NOT NULL,
    Team_1_Score int,
    Team_2_Score int,
    Map varchar(255),
    PRIMARY KEY (MatchID)
);

CREATE TABLE Players (
    PlayerID varchar(255) NOT NULL,
    PRIMARY KEY (PlayerID)
);

CREATE TABLE PlayerStats(
    PlayerID varchar(255) NOT NULL,
    MatchID varchar(255) NOT NULL,
    Kills int,
    Assists int,
    Deaths int,
    Headshots int,
    HeadshotsPerc float,
    KR_Ratio float,
    KD_Ratio float,
    TripleKills int,
    QuadroKills int,
    PentaKills int,
    MVPs int,
    PRIMARY KEY (PlayerID, MatchID),
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID)
);