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


    def listLocation(self, location):
        try:
            return os.listdir(location)
        except FileNotFoundError:
            pass

        return []
