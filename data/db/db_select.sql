USE Football;

DROP VIEW IF EXISTS MPSG;

CREATE VIEW MPSG AS SELECT PlayerID, Points, GameStatus, SoccerGameDate FROM MappingPlayersSoccerGames MPSG
JOIN SoccerGames SG
ON MPSG.SoccerGameID = SG.SoccerGameID
AND SG.SoccerGameDate >= '20170101'
AND SG.SoccerGameDate <= '20171231';

SELECT * FROM MPSG;

SELECT PlayerName AS 'Name',
IFNULL(WINS.Wins, 0) AS 'Wins', DRAWS.Draws AS 'Draws', LOSES.Loses AS 'Loses', COUNT(GameStatus) AS 'Total Games',
CONCAT(CAST(AVG(GameStatus = 'W') * 100 AS DECIMAL(5, 2)), '%') AS 'Victory Rate', CONCAT(CAST((SUM(Points) / (COUNT(Points) * 3)) * 100 AS DECIMAL(5, 2)), '%') AS 'Score Rate'

FROM MPSG -- MappingPlayersSoccerGames MPSG
-- 
-- JOIN SoccerGames SG
-- ON MPSG.SoccerGameID = SG.SoccerGameID
-- AND SG.SoccerGameDate > '17-06-19'

JOIN Players P
ON MPSG.PlayerID = P.PlayerID

LEFT JOIN (SELECT PlayerID, COUNT(GameStatus) AS Wins FROM MPSG WHERE GameStatus = 'W' GROUP BY PlayerID) WINS
ON MPSG.PlayerID = WINS.PlayerID

LEFT JOIN (SELECT PlayerID, COUNT(GameStatus) AS Draws FROM MPSG WHERE GameStatus = 'D' GROUP BY PlayerID) DRAWS
ON MPSG.PlayerID = DRAWS.PlayerID

LEFT JOIN (SELECT PlayerID, COUNT(GameStatus) AS Loses FROM MPSG WHERE GameStatus = 'L' GROUP BY PlayerID) LOSES
ON MPSG.PlayerID = LOSES.PlayerID

GROUP BY MPSG.PlayerID

-- HAVING SG.SoccerGameDate > CONVERT('2014-06-24', DATE)
;


SELECT * FROM players;

SELECT PlayerID
FROM Players
WHERE PlayerName = 'Кленов'