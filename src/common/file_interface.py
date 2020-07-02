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


    def wipe(self, path):
        try:
            with open(path, 'w') as filee:
                pass
        except FileNotFoundError:
            pass
