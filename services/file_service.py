from os import path


class FileService:

    def write(self, filePath, data):
        with open(filePath, 'w+') as file:
            file.write(data)


    def read(self, filePath, defaultData = ''):
        dataStr = ''

        if not path.exists(filePath):
            return dataStr

        with open(filePath, 'r') as file:
            dataStr = file.read()

        return dataStr
