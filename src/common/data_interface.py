import sqlite3


class DataInterface:

    def __init__(self, databasePath):
        self.database = sqlite3.connect(databasePath)
        self.cursor =  self.database.cursor()


    def insert(self, tableName, tableHeader, data):
        self.createTable(tableName, tableHeader, 0)

        self.cursor.executemany("INSERT OR REPLACE INTO '{}' (timestamp, open, high, low, close) VALUES (?, ?, ?, ?, ?)".format(tableName), data)

        self.database.commit()


    def createTable(self, name, header, index=-1):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS '{}' {}".format(name, header))

        if index != -1:
            self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_timestamp on '{}' (timestamp)".format(name))


    def tableExists(self, name):
        self.cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'".format(name))

        return self.cursor.fetchone()[0] != 0


    def select(self, tableName, numLastEntries=0):
        if not self.tableExists(tableName):
            return []

        if not numLastEntries:
            self.cursor.execute("SELECT * FROM '{}'".format(tableName))
        else:
            self.cursor.execute('''SELECT * FROM
                                   (SELECT * FROM '{}' ORDER BY timestamp DESC LIMIT {})
                                   ORDER BY timestamp ASC'''.format(tableName, numLastEntries))

        return self.cursor.fetchall()
