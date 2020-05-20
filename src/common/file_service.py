import os


class FileService:

    def write(self, path, data):
        locationItems = path.strip().strip('/').split('/')[: - 1]

        location = ''
        for directory in locationItems:
            location += directory + '/'
            if not os.path.exists(location):
                os.mkdir(location)

        with open(path, 'w+') as filee:
            filee.write(data)


    def read(self, path):
        with open(path, 'r') as filee:
            return filee.read()

        return ''


    def readLines(self, path):
        with open(path, 'r') as filee:
            return filee.readlines()

        return []


    def readLastLines(self, path, numLastLines, maxLineLength=70):
        with open(path, 'rb') as filee:
            try:
                filee.seek(-(numLastLines * maxLineLength), 2)
            except OSError:
                return []

            return filee.readlines()[-numLastLines :]

        return []


    def listLocation(self, location):
        try:
            return os.listdir(location)
        except FileNotFoundError:
            pass

        return []
