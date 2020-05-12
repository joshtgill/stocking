import os


class FileService:

    def write(self, filePath, data, clearBefore=False):
        locationItems = filePath.strip().strip('/').split('/')[: - 1]

        directoryPath = ''
        for directory in locationItems:
            directoryPath += directory + '/'
            if not os.path.exists(directoryPath):
                os.mkdir(directoryPath)

        if clearBefore:
            open(filePath, 'w').close()

        with open(filePath, 'a+') as filee:
            filee.write(data)


    def read(self, path):
        with open(path, 'r') as filee:
            return filee.read()

        return ''


    def readLines(self, filePath):
        with open(filePath, 'r') as filee:
            return filee.readlines()

        return []


    def readLastLine(self, filePath, maxLineLength=100):
        with open(filePath, 'rb') as filee:
            filee.seek(-maxLineLength, 2)
            return filee.readlines()[-1].decode()

        return ''


    def listDirectory(self, location):
        try:
            return os.listdir(location)
        except FileNotFoundError:
            pass

        return []
