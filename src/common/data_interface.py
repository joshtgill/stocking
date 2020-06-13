import sqlite3


class DataInterface:

    def __init__(self, databasePath):
        self.database = sqlite3.connect(databasePath)
        self.cursor =  self.database.cursor()


    def insert(self, tableName, tableHeader, data):
        self.createTable(tableName, tableHeader)

        self.cursor.executemany("INSERT INTO '{}' VALUES (?, ?, ?, ?, ?)".format(tableName), data)

        self.database.commit()


    def createTable(self, name, header):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS '{}' {}".format(name, header))


    def select(self, tableName, numLastEntries=0):
        data = []

        if not numLastEntries:
            self.cursor.execute("SELECT * FROM '{}'".format(tableName))
        else:
            self.cursor.execute('''IF (EXISTS SELECT * FROM
                                   (SELECT * FROM '{}' ORDER BY timestamp DESC LIMIT {})
                                   ORDER BY timestamp ASC)'''.format(tableName, numLastEntries))

        return self.cursor.fetchall()
