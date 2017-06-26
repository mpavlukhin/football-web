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

ALTER TABLE `MappingPlayersSoccerGames` ADD CONSTRAINT `MappingPlayersSoccerGames_PlayerID` FOREIGN KEY (`PlayerID`) REFERENCES `Players`(`PlayerID`);
ALTER TABLE `MappingPlayersSoccerGames` ADD CONSTRAINT `MappingPlayersSoccerGames_SoccerGameID` FOREIGN KEY (`SoccerGameID`) REFERENCES `SoccerGames`(`SoccerGameID`);

-- Insert data into tables
INSERT INTO Players (PlayerName) VALUES ('Кленов'), ('Игнатов'), ('Макс'), ('Глеб');
INSERT INTO SoccerGames (SoccerGameDate) VALUES ('17-06-19'), ('17-06-22'), ('17-06-26'); -- YYYY-MM-DD

INSERT INTO MappingPlayersSoccerGames VALUES (1, 1, 10, 'L'), (1, 2, 7, 'W'), (1, 3, 8, 'W'); -- for Кленов
INSERT INTO MappingPlayersSoccerGames VALUES (4, 1, 10, 'L'), (4, 2, 7, 'W'), (4, 3, 7, 'L'); -- for Глеб


-- Select data from tables
SELECT * FROM Players
ORDER BY PlayerID;

SELECT * FROM SoccerGames
ORDER BY SoccerGameDate;

SELECT MPSG.PlayerID, PlayerName,
MPSG.SoccerGameID, SG.SoccerGameDate,
MPSG.Points, MPSG.GameStatus
FROM MappingPlayersSoccerGames MPSG
JOIN Players P
ON MPSG.PlayerID = P.PlayerID
JOIN SoccerGames SG
ON MPSG.SoccerGameID = SG.SoccerGameID;