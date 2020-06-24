import sqlite3


class DataInterface:

    def __init__(self, databasePath):
        self.database = sqlite3.connect(databasePath)
        self.cursor =  self.database.cursor()


    def insert(self, tableName, tableHeader, data):
        self.createTable(tableName, tableHeader, 0)

        self.cursor.executemany("INSERT OR REPLACE INTO '{}' {} VALUES (?, ?, ?, ?, ?)".format(tableName, tableHeader), data)

        self.database.commit()


    def createTable(self, name, header, uniqueIndex=-1):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS '{}' {}".format(name, header))

        if uniqueIndex != -1:
            uniqueIndexName = header[1 : -1].replace(' ', '').split(',')[uniqueIndex]
            self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_{} on '{}' ({})".format(uniqueIndexName, name, uniqueIndexName))


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
