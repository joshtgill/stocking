import sqlite3


class DatabaseInterface:

    def __init__(self, databasePath):
        self.database = sqlite3.connect(databasePath)
        self.cursor =  self.database.cursor()


    def tableExists(self, name):
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master
                                WHERE type='table' AND name='{}' '''.format(name))

        return self.cursor.fetchone()[0] != 0


    def createTable(self, tableName, columnHeader):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS '{}'
                                {} '''.format(tableName, columnHeader))
        self.database.commit()


    def insert(self, tableName, columnHeader, data):
        generalColumnHeader = '({})'.format(','.join(['?' for i in range(len(columnHeader.split(',')))]))

        self.cursor.executemany(''' INSERT OR REPLACE INTO '{}'
                                    {}
                                    VALUES {} '''.format(tableName, columnHeader, generalColumnHeader), data)
        self.database.commit()


    def select(self, tableName, executeStr):
        if not self.tableExists(tableName):
            return []

        self.cursor.execute(executeStr)

        return self.cursor.fetchall()


    def selectAll(self, tableName):
        executeStr = ''' SELECT * FROM '{}' '''.format(tableName)

        return self.select(tableName, executeStr)


    def selectPeriod(self, tableName, start, end):
        executeStr = ''' SELECT * FROM '{}'
                         WHERE timestamp BETWEEN '{}' AND '{}' '''.format(tableName, start, end)

        return self.select(tableName, executeStr)


    def selectLastRows(self, tableName, numLastRows):
        executeStr = ''' SELECT * FROM
                         (SELECT * FROM '{}'
                         ORDER BY timestamp DESC LIMIT {})
                         ORDER BY timestamp ASC '''.format(tableName, numLastRows)

        return self.select(tableName, executeStr)
