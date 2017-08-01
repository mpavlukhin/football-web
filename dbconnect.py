import MySQLdb


def connection(is_first=False):
    conn = MySQLdb.connect(host="e7qyahb3d90mletd.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
                           user="vqpq0re2r4unjcpm",
                           passwd="mu7nnhusacy3zijr",
                           db='yksc2nhvbiqhmiow',
                           charset='utf8')

    c = conn.cursor()

    return c, conn


def db_existence_checker(db_name):
    c, conn = connection(True)

    cmd_use_db = 'USE {:s}'.format(db_name)

    c.execute(cmd_use_db)

    cmd_check_existence = 'SHOW TABLES'

    c.execute(cmd_check_existence)

    db_any_table_name = c.fetchone()

    if db_any_table_name is not None:
        return True

    return False


def db_cleaner(c, conn):
    # 'drop' database Football
    c.execute("DROP TABLE WebServiceUsers")
    c.execute("DROP TABLE MappingPlayersSoccerGames")
    c.execute("SET FOREIGN_KEY_CHECKS = 0")
    c.execute("DROP TABLE SoccerGames")
    c.execute("DROP TABLE Players")
    c.execute("SET FOREIGN_KEY_CHECKS = 1")


def db_creation_handler(c, conn):
    c.execute("CREATE TABLE `Players` ("
              "`PlayerID` int NOT NULL AUTO_INCREMENT,"
              "`PlayerName` varchar(20) NOT NULL UNIQUE,"
              "PRIMARY KEY (`PlayerID`));")
    
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
    c, conn = connection()
    db_creation_handler(c, conn)
    print("Database successfully created!")


def recreateDB():
    c, conn = connection()
    db_cleaner(c, conn)
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

