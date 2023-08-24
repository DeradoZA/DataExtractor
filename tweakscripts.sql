select count(*) from matches 
select count(*) from players

select * from playerstats where MatchID = "1-00010bb0-f6e0-40e9-b743-67d0ede4cb2a-1-1"

select steamID, playerid from players where steamID = "76561198042329439"
select steamID, playerid from players where playerID  = "0654d1a3-5827-4a6f-a3e2-c40fba80b840"

CREATE TABLE PlayerELOs(
    steamID varchar(255) NOT NULL,
    MatchID varchar(255) NOT NULL,
    MatchTime bigint(20),
    ELO int,
    PRIMARY KEY(steamID, MatchID)
)

drop table if exists PlayerELOs;

UPDATE matches
SET matchid = SUBSTRING(matchid, 1, LENGTH(matchid) - 4)
WHERE matchid LIKE '%-1-1';

UPDATE playerstats
SET matchid = SUBSTRING(matchid, 1, LENGTH(matchid) - 4)
WHERE matchid LIKE '%-1-1';

UPDATE matches
SET matchid = SUBSTRING(matchid, 1, LENGTH(matchid) - 4)
WHERE matchid LIKE '%-1-2';

UPDATE playerstats
SET matchid = SUBSTRING(matchid, 1, LENGTH(matchid) - 4)
WHERE matchid LIKE '%-1-2';

SET FOREIGN_KEY_CHECKS = 0;
SET FOREIGN_KEY_CHECKS = 1;

SELECT steamID, COUNT(*) as GAMESPLAYED
FROM PLAYERSTATS
GROUP BY steamID
HAVING COUNT(*) > 3;
