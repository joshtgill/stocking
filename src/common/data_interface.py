import sqlite3


class DataInterface:

    def __init__(self, databasePath):
        self.database = sqlite3.connect(databasePath)
        self.cursor =  self.database.cursor()


    def createTable(self, name, header):
        if not self.tableExists(name):
            self.cursor.execute("CREATE TABLE {} {}".format(name, header))


    def tableExists(self, name):
        self.cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'".format(name))

        return self.cursor.fetchone()[0] != 0


    def insert(self, tableName, tableHeader, data):
        self.createTable(tableName, tableHeader)

        self.cursor.executemany("INSERT INTO {} VALUES (?, ?, ?, ?, ?)".format(tableName), data)

        self.database.commit()


    def select(self, tableName, numLastEntries=0):
        data = []

        if not self.tableExists(tableName):
            return data

        if numLastEntries:
            self.cursor.execute('''SELECT * FROM
                                   (SELECT * FROM {} ORDER BY timestamp DESC LIMIT {})
                                   ORDER BY timestamp ASC'''.format(tableName, numLastEntries))
        else:
            self.cursor.execute("SELECT * FROM {}".format(tableName))

        return self.cursor.fetchall()
