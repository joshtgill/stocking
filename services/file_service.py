from os import path


class FileService:

    def __init__(self, filePath):
        self.filePath = filePath


    def write(self, data):
        with open(self.filePath, 'w+') as file:
            file.write(data)


    def read(self, defaultData = ''):
        dataStr = ''

        # Verify path exists
        if not path.exists(self.filePath):
            return dataStr

        with open(self.filePath, 'r') as file:
            dataStr = file.read()

        return dataStr
