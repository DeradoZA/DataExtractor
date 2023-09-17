from mysql.connector import connect, Error, errorcode

class DBConnectionCreator:
    def __init__(self, user, db, password) -> None:
        self.user = user
        self.password = password
        self.db = db

    def dbConnection(self):
        try:
            connection = connect(
                host = 'localhost',
                user = self.user,
                password = self.password,
                database = self.db
            )
        except Error as e:
            return e
        
        cursor = connection.cursor()

        return connection, cursor