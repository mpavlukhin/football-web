import MySQLdb


def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "football64",
                           db = "Football",
                           charset='utf8')
    c = conn.cursor()

    return c, conn


def recreateDB():
    c, conn = connection()
    c.execute("DROP DATABASE IF EXISTS Football")
    c.execute("CREATE DATABASE Football")
    c.execute("USE Football")
    c.execute("CREATE TABLE `Players` (	`PlayerID` int NOT NULL AUTO_INCREMENT,	`PlayerName` varchar(20) NOT NULL UNIQUE,PRIMARY KEY (`PlayerID`));")
    c.execute("CREATE TABLE `SoccerGames` ("
	"`SoccerGameID` int NOT NULL AUTO_INCREMENT,"
	"`SoccerGameDate` DATE NOT NULL UNIQUE,"
	"PRIMARY KEY (`SoccerGameID`)"
    ");")
    c.execute("CREATE TABLE `MappingPlayersSoccerGames` ("
	"`PlayerID` int NOT NULL,"
	"`SoccerGameID` int NOT NULL,"
	"`Points` int NOT NULL,"
    "`GameStatus` char(1) NOT NULL"
    ");")
    c.execute("ALTER TABLE `MappingPlayersSoccerGames` ADD CONSTRAINT `MappingPlayersSoccerGames_PlayerID` FOREIGN KEY (`PlayerID`) REFERENCES `Players`(`PlayerID`);")
    c.execute("ALTER TABLE `MappingPlayersSoccerGames` ADD CONSTRAINT `MappingPlayersSoccerGames_SoccerGameID` FOREIGN KEY (`SoccerGameID`) REFERENCES `SoccerGames`(`SoccerGameID`);")
    conn.autocommit("Recreating DB")
    print("Database successfully recreated!")