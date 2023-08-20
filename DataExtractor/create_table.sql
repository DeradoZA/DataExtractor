DROP TABLE IF EXISTS PlayerStats;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Matches;


CREATE TABLE Matches (
    MatchID varchar(255) NOT NULL,
    Team_1_Score int,
    Team_2_Score int,
    Map varchar(255),
    MatchTime int,
    PRIMARY KEY (MatchID)
);

CREATE TABLE Players (
    steamID varchar(255) NOT NULL,
    playerID varchar(255),
    PRIMARY KEY (steamID)
);

CREATE TABLE PlayerStats(
    steamID varchar(255) NOT NULL,
    MatchID varchar(255) NOT NULL,
    Team int,
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
    KAST float,
    EntryKills int,
    BombDefused int,
    BombPlanted int,
    RWS float,
    Rating float,
    Rating2 float,
    ATD float,
    ADR float,
    TradeKills int,
    ClutchWinPer float,
    totalSmokes int,
    totalFalshes int,
    totalFire int,
    totalHE int,
    PRIMARY KEY (steamID, MatchID),
    FOREIGN KEY (steamID) REFERENCES Players(steamID),
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID)
);