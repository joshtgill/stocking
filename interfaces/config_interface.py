from services.file_service import FileService
import json


class ConfigInterface:

    def __init__(self, fileService, configFileName):
        self.fileService = fileService

        self.config = json.loads(self.fileService.read(configFileName, '{}'))


    def get(self, path, Obj = None):
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
