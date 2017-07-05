-- Creating of DB
DROP DATABASE IF EXISTS Football;
CREATE DATABASE Football;

-- Creating of tables
USE Football;

CREATE TABLE `Players` (
	`PlayerID` int NOT NULL AUTO_INCREMENT,
	`PlayerName` varchar(20) NOT NULL UNIQUE,
	PRIMARY KEY (`PlayerID`)
);

CREATE TABLE `SoccerGames` (
	`SoccerGameID` int NOT NULL AUTO_INCREMENT,
	`SoccerGameDate` DATE NOT NULL UNIQUE,
	PRIMARY KEY (`SoccerGameID`)
);

CREATE TABLE `MappingPlayersSoccerGames` (
	`PlayerID` int NOT NULL,
	`SoccerGameID` int NOT NULL,
	`Points` int NOT NULL,
    `GameStatus` char(1) NOT NULL
);

CREATE TABLE `WebServiceUsers` (
	`Username` varchar(20) NOT NULL UNIQUE,
	`Password` varchar(20) NOT NULL,
);

ALTER TABLE `MappingPlayersSoccerGames` ADD CONSTRAINT `MappingPlayersSoccerGames_PlayerID` FOREIGN KEY (`PlayerID`) REFERENCES `Players`(`PlayerID`);
ALTER TABLE `MappingPlayersSoccerGames` ADD CONSTRAINT `MappingPlayersSoccerGames_SoccerGameID` FOREIGN KEY (`SoccerGameID`) REFERENCES `SoccerGames`(`SoccerGameID`);

-- Insert data into tables
INSERT INTO Players (PlayerName) VALUES ('Кленов'), ('Игнатов'), ('Макс'), ('Глеб');
INSERT INTO SoccerGames (SoccerGameDate) VALUES ('17-06-19'), ('17-06-22'), ('17-06-26'); -- YYYY-MM-DD

-- Select data from tables
SELECT * FROM Players
ORDER BY PlayerID;

SELECT * FROM SoccerGames
ORDER BY SoccerGameDate;

SELECT * FROM MappingPlayersSoccerGames;

-- Insert test data
INSERT INTO SoccerGames (SoccerGameDate) VALUES ('14-06-19'), ('15-06-22'), ('16-06-26'), ('14-06-11'); -- YYYY-MM-DD

INSERT INTO MappingPlayersSoccerGames VALUES (1, 4, 1, 'L'), (1, 5, 1, 'D'), (1, 6, 3, 'W'), (1, 7, 3, 'W'); -- for Кленов
INSERT INTO MappingPlayersSoccerGames VALUES (4, 4, 3, 'W'), (4, 5, 1, 'W'), (4, 6, 0, 'L'); -- for Глеб

-- 1) select year, day month
SELECT MPSG.PlayerID, P.PlayerName,
MPSG.SoccerGameID, SG.SoccerGameDate,
MPSG.Points, MPSG.GameStatus
FROM MappingPlayersSoccerGames MPSG
JOIN Players P
ON MPSG.PlayerID = P.PlayerID
JOIN SoccerGames SG
ON MPSG.SoccerGameID = SG.SoccerGameID
WHERE P.PlayerName = 'Глеб'
AND SG.SoccerGameDate < CONVERT('2017-06-26', DATE)
AND SG.SoccerGameDate > CONVERT('2017-06-19', DATE);

-- 2) select year
SELECT MPSG.PlayerID, P.PlayerName,
MPSG.SoccerGameID, SG.SoccerGameDate,
MPSG.Points, MPSG.GameStatus
FROM MappingPlayersSoccerGames MPSG
JOIN Players P
ON MPSG.PlayerID = P.PlayerID
JOIN SoccerGames SG
ON MPSG.SoccerGameID = SG.SoccerGameID
WHERE P.PlayerName = 'Глеб'
AND SG.SoccerGameDate < CONVERT('2018-0-0', DATE)
AND SG.SoccerGameDate > CONVERT('2017-0-0', DATE)
ORDER BY SoccerGameDate DESC;

SELECT PlayerName FROM Players;

SELECT MPSG.PlayerID, PlayerName, MPSG.SoccerGameID, SG.SoccerGameDate, MPSG.Points, MPSG.GameStatus
FROM MappingPlayersSoccerGames MPSG
JOIN Players P ON MPSG.PlayerID = P.PlayerID
JOIN SoccerGames SG ON MPSG.SoccerGameID = SG.SoccerGameID
WHERE P.PlayerName = 'Глеб'
AND SG.SoccerGameDate <= CONVERT('20170627', DATE)
AND SG.SoccerGameDate >= CONVERT('20170607', DATE)
ORDER BY PlayerName AND SoccerGameDate;

SELECT MPSG.PlayerID, PlayerName, MPSG.SoccerGameID, SG.SoccerGameDate, MPSG.Points, MPSG.GameStatus
FROM MappingPlayersSoccerGames MPSG
JOIN Players P ON MPSG.PlayerID = P.PlayerID
JOIN SoccerGames SG ON MPSG.SoccerGameID = SG.SoccerGameID
WHERE P.PlayerName = 'Глеб'
AND SG.SoccerGameDate <= CONVERT('20170627', DATE)
AND SG.SoccerGameDate >= CONVERT('20170627', DATE)
ORDER BY PlayerName AND SoccerGameDate;

SELECT MPSG.PlayerID, P.PlayerName,
MPSG.SoccerGameID, SG.SoccerGameDate,
MPSG.Points, MPSG.GameStatus
FROM MappingPlayersSoccerGames MPSG
JOIN SoccerGames SG
ON MPSG.SoccerGameID = SG.SoccerGameID

WHERE P.PlayerName = 'Глеб'
ORDER BY SG.SoccerGameDate;

SELECT * FROM MappingPlayersSoccerGames
ORDER BY PlayerID;

SELECT * FROM MappingPlayersSoccerGames;

SELECT COUNT(PlayerID)
FROM MappingPlayersSoccerGames
WHERE PlayerID = 4;

SELECT COUNT(PlayerID)
FROM MappingPlayersSoccerGames
WHERE PlayerID = 4;

SELECT AVG(Points)
FROM MappingPlayersSoccerGames
WHERE PlayerID = 4;

SELECT AVG (a.Points)
FROM (SELECT Points FROM MappingPlayersSoccerGames) a;

SELECT * FROM MappingPlayersSoccerGames
WHERE GameStatus = 'W';

SELECT MPSG.PlayerID, PlayerName, COUNT(GameStatus), AVG (Points)
FROM MappingPlayersSoccerGames MPSG
JOIN Players P
ON MPSG.PlayerID = P.PlayerID
GROUP BY PlayerID
HAVING COUNT(GameStatus) >= 6;

SELECT AVG(Sel.GS)
FROM (SELECT MPSG.PlayerID, PlayerName, COUNT(GameStatus) as GS
FROM MappingPlayersSoccerGames MPSG
JOIN Players P
ON MPSG.PlayerID = P.PlayerID
GROUP BY PlayerID
HAVING COUNT(GameStatus) >= 6) Sel
GROUP BY Sel.PlayerID;

SELECT PlayerName AS 'Name', WIN.Wins, AVG (Points), AVG(GameStatus = 'W')
FROM MappingPlayersSoccerGames MPSG
JOIN Players P
ON MPSG.PlayerID = P.PlayerID
JOIN (SELECT PlayerID, COUNT(GameStatus) AS Wins FROM MappingPlayersSoccerGames WHERE GameStatus = 'W' GROUP BY PlayerID) WIN
ON MPSG.PlayerID = WIN.PlayerID
GROUP BY MPSG.PlayerID
HAVING COUNT(GameStatus) >= 6;

SELECT PlayerID, COUNT(GameStatus) AS Wins FROM MappingPlayersSoccerGames WHERE GameStatus = 'W' GROUP BY PlayerID;

SELECT COUNT(GameStatus)
FROM MappingPlayersSoccerGames
WHERE GameStatus = 'W';

SELECT PlayerName AS 'Name', Wins, AVG (Points), AVG(GameStatus = 'W')
FROM MappingPlayersSoccerGames MPSG
JOIN Players P
ON MPSG.PlayerID = P.PlayerID
GROUP BY MPSG.PlayerID
HAVING COUNT(GameStatus) >= 6;

SELECT PlayerName, A.GS FROM Players P
LEFT JOIN (SELECT PlayerID, COUNT(GameStatus) AS GS FROM MappingPlayersSoccerGames MPSG WHERE GameStatus = 'W') AS A
ON P.PlayerID = A.PlayerID;

SELECT COUNT(IF(GameStatus = 'W', 'W', 'L'))
FROM MappingPlayersSoccerGames;

SELECT PlayerName AS 'Name',
WINS.Wins AS 'Wins', DRAWS.Draws AS 'Draws', LOSES.Loses AS 'Loses', COUNT(GameStatus) AS 'Total Games',
AVG(GameStatus = 'W') AS 'Victory Rate', AVG (Points) AS 'Score Rate'
FROM MappingPlayersSoccerGames MPSG

JOIN Players P
ON MPSG.PlayerID = P.PlayerID

JOIN (SELECT PlayerID, COUNT(GameStatus) AS Wins FROM MappingPlayersSoccerGames WHERE GameStatus = 'W' GROUP BY PlayerID) WINS
ON MPSG.PlayerID = WINS.PlayerID

JOIN (SELECT PlayerID, COUNT(GameStatus) AS Draws FROM MappingPlayersSoccerGames WHERE GameStatus = 'D' GROUP BY PlayerID) DRAWS
ON MPSG.PlayerID = DRAWS.PlayerID

JOIN (SELECT PlayerID, COUNT(GameStatus) AS Loses FROM MappingPlayersSoccerGames WHERE GameStatus = 'L' GROUP BY PlayerID) LOSES
ON MPSG.PlayerID = LOSES.PlayerID

GROUP BY MPSG.PlayerID

HAVING MappingPlayersSoccerGames.SoccerGameDate > CONVERT('2014-06-24', DATE)
;

SELECT * FROM MappingPlayersSoccerGames MPSG
JOIN SoccerGames SG
ON MPSG.SoccerGameID = SG.SoccerGameID
AND SG.SoccerGameDate >= '17-06-19';

DROP VIEW MPSG;

CREATE VIEW MPSG AS SELECT PlayerID, Points, GameStatus, SoccerGameDate FROM MappingPlayersSoccerGames MPSG
JOIN SoccerGames SG
ON MPSG.SoccerGameID = SG.SoccerGameID
AND SG.SoccerGameDate > '17-06-19';

SELECT * FROM MPSG;

SELECT PlayerName AS 'Name',
WINS.Wins AS 'Wins', DRAWS.Draws AS 'Draws', LOSES.Loses AS 'Loses',
COUNT(GameStatus) AS 'Total Games',
AVG(GameStatus = 'W') AS 'Victory Rate', (SUM(Points) / (COUNT(Points) * 3)) AS 'Score Rate'

FROM MPSG

JOIN Players P
ON MPSG.PlayerID = P.PlayerID

JOIN (SELECT PlayerID, COUNT(GameStatus) AS Wins FROM MPSG WHERE GameStatus = 'W' GROUP BY PlayerID) WINS
ON MPSG.PlayerID = WINS.PlayerID

JOIN (SELECT PlayerID, COUNT(GameStatus) AS Draws FROM MPSG WHERE GameStatus = 'D' GROUP BY PlayerID) DRAWS
ON MPSG.PlayerID = DRAWS.PlayerID

JOIN (SELECT PlayerID, COUNT(GameStatus) AS Loses FROM MPSG WHERE GameStatus = 'L' GROUP BY PlayerID) LOSES
ON MPSG.PlayerID = LOSES.PlayerID

GROUP BY MPSG.PlayerID

HAVING SG.SoccerGameDate > CONVERT('2014-06-24', DATE)
;

DROP VIEW IF EXISTS MPSG;

CREATE VIEW MPSG AS SELECT PlayerID, Points, GameStatus, SoccerGameDate FROM MappingPlayersSoccerGames MPSG
JOIN SoccerGames SG
ON MPSG.SoccerGameID = SG.SoccerGameID
AND SG.SoccerGameDate >= '20170101'
AND SG.SoccerGameDate <= '20171231';

SELECT * FROM MPSG;

SELECT PlayerName AS 'Name',
WINS.Wins AS 'Wins', DRAWS.Draws AS 'Draws', LOSES.Loses AS 'Loses', COUNT(GameStatus) AS 'Total Games',
AVG(GameStatus = 'W') AS 'Victory Rate', (SUM(Points) / (COUNT(Points) * 3)) AS 'Score Rate'

FROM MPSG

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


SELECT PlayerName AS 'Name',
WINS.Wins AS 'Wins',
AVG(GameStatus = 'W') AS 'Victory Rate', (SUM(Points) / (COUNT(Points) * 3)) AS 'Score Rate'

FROM MappingPlayersSoccerGames MPSG

JOIN SoccerGames SG
ON MPSG.SoccerGameID = SG.SoccerGameID
AND SG.SoccerGameDate > '17-06-22'

JOIN Players P
ON MPSG.PlayerID = P.PlayerID

JOIN (SELECT PlayerID, COUNT(GameStatus) AS Wins FROM MappingPlayersSoccerGames WHERE GameStatus = 'W' GROUP BY PlayerID) WINS
ON MPSG.PlayerID = WINS.PlayerID

GROUP BY MPSG.PlayerID

-- HAVING SG.SoccerGameDate > CONVERT('2014-06-24', DATE)
;

SELECT * FROM Players;

SELECT PlayerID, Points, GameStatus, SG.SoccerGameDate FROM MappingPlayersSoccerGames MSG
JOIN SoccerGames SG
ON MSG.SoccerGameID = SG.SoccerGameID
WHERE PlayerID = 1 and SoccerGameDate <= '15-01-01' and SoccerGameDate >= '14-01-01'
ORDER BY PlayerID;

