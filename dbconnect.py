import MySQLdb


def connection(is_first=False):
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "football64",
                           charset='utf8')

    if not is_first:
        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="football64",
                               db='Football',
                               charset='utf8')

    c = conn.cursor()

    return c, conn


def db_existence_checker(db_name):
    c, conn = connection(True)
    cmd_check_existence = 'SELECT SCHEMA_NAME ' \
                          'FROM INFORMATION_SCHEMA.SCHEMATA ' \
                          'WHERE SCHEMA_NAME = "{:s}"'.format(db_name)

    c.execute(cmd_check_existence)

    db_schema_name = c.fetchone()

    if db_schema_name is not None:
        return True

    return False


def db_creation_handler(c, conn):
    c.execute("DROP DATABASE IF EXISTS Football")
    c.execute("CREATE DATABASE Football")
    c.execute("USE Football")
    c.execute(
        "CREATE TABLE `Players` (	`PlayerID` int NOT NULL AUTO_INCREMENT,	`PlayerName` varchar(20) NOT NULL UNIQUE,PRIMARY KEY (`PlayerID`));")
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

    c.execute("CREATE TABLE `WebServiceUsers` ("
              "`Username` varchar(20) NOT NULL UNIQUE,"
              "`Password` varchar(20) NOT NULL"
              ");")

    c.execute(
        "ALTER TABLE `MappingPlayersSoccerGames` ADD CONSTRAINT `MappingPlayersSoccerGames_PlayerID` FOREIGN KEY (`PlayerID`) REFERENCES `Players`(`PlayerID`);")
    c.execute(
        "ALTER TABLE `MappingPlayersSoccerGames` ADD CONSTRAINT `MappingPlayersSoccerGames_SoccerGameID` FOREIGN KEY (`SoccerGameID`) REFERENCES `SoccerGames`(`SoccerGameID`);")
    c.execute(
        "ALTER TABLE `MappingPlayersSoccerGames` ADD UNIQUE `MappingPlayersSoccerGames_UniquePlayerGame` (`PlayerID`, `SoccerGameID`);")
    c.execute("INSERT INTO WebServiceUsers VALUES ('admin', 'football64');")
    conn.autocommit("Recreating DB")


def create_db():
    c, conn = connection(True)
    db_creation_handler(c, conn)
    print("Database successfully created!")


def recreateDB():
    c, conn = connection()
    db_creation_handler(c, conn)
    print("Database successfully recreated!")


def getWebServiceUsers():
    c, conn = connection()
    list = [[]]
    c.execute("SELECT * FROM WebServiceUsers")
    for (user, password) in c:
        list.append([user, password])
    list.pop(0)
    return list

