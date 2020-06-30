import sqlite3


class DataInterface:

    def __init__(self, databasePath):
        self.database = sqlite3.connect(databasePath)
        self.cursor =  self.database.cursor()


    def insert(self, tableName, data):
        self.createTable(tableName)

        self.cursor.executemany("INSERT OR REPLACE INTO '{}' (timestamp, open, high, low, close) VALUES (?, ?, ?, ?, ?)".format(tableName), data)

        self.database.commit()


    def createTable(self, name):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS '{}' (timestamp, open, high, low, close, UNIQUE(timestamp))".format(name))


    def tableExists(self, name):
        self.cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'".format(name))

        return self.cursor.fetchone()[0] != 0


    def select(self, tableName, start='', end=''):
        if not self.tableExists(tableName):
            return []

        if not start and not end:
            self.cursor.execute("SELECT * FROM '{}'".format(tableName))
        else:
            self.cursor.execute("SELECT * FROM '{}' WHERE timestamp BETWEEN '{}' AND '{}'".format(tableName, start, end))

        return self.cursor.fetchall()
