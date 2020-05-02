import json
from os import path


class DataService:

    def loadConfig(self, configFileName):
        self.config = json.loads(self.read(configFileName, '{}'))


    def configGet(self, path, Obj = None):
        # Make list from path string
        pathList = path.strip().strip('/').split('/')

        # Traverse config down path
        configRunner = self.config
        for pathItem in pathList:
            if '[' in pathItem:
                index = int(pathItem[pathItem.find('[') + 1 : pathItem.find(']')])
                pathItem = pathItem[0 : pathItem.index('[')]
                configRunner = configRunner.get(pathItem)[index]
            else:
                configRunner = configRunner.get(pathItem)

        # If None, then assume value is an empty list
        if configRunner == None:
            return []

        # Build found config
        if isinstance(configRunner, list):
            itemList = []
            for item in configRunner:
                if Obj is not None:
                    obj = Obj()
                    obj.deserialize(item)
                    itemList.append(obj)
                else:
                    itemList.append(item)

            return itemList
        else:
            if Obj is not None:
                obj = Obj()
                obj.deserialize(configRunner)

                return obj
            else:
                return configRunner


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
