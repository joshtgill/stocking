import os


class FileInterface:

    def write(self, path, data):
        locationDirectories = path.strip().strip('/').split('/')[: - 1]

        locationStr = ''
        for directory in locationDirectories:
            locationStr += directory + '/'
            if not os.path.exists(locationStr):
                os.mkdir(locationStr)

        with open(path, 'a+') as filee:
            filee.write(data)


    def read(self, path):
        with open(path, 'r') as filee:
            return filee.read()

        return ''


    def readLines(self, path):
        with open(path, 'r') as filee:
            return filee.readlines()

        return []


    def readLastLines(self, path, numLastLines, maxLineLength = 70):
        try:
            with open(path, 'rb') as filee:
                filee.seek(-(numLastLines * maxLineLength), 2)

                return filee.readlines()[-numLastLines :]
        except:
            pass

        return []


    def listLocation(self, location):
        try:
            return os.listdir(location)
        except FileNotFoundError:
            pass

        return []
