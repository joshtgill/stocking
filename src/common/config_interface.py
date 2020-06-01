import json


class ConfigInterface:

    def __init__(self, fileService):
        self.fileService = fileService


    def loadConfig(self, configPath):
        return json.loads(self.fileService.read(configPath))


    def loadQueryConfig(self, configPath):
        config = self.loadConfig(configPath)

        # Load any config vars
        configVarMap = {'ALL_SYMBOLS': 'data/symbols/all_symbols.json'}
        symbols = config.get('symbols')
        if not isinstance(symbols, list):
            if symbols in configVarMap.keys():  # Symbols value is config var
                symbols = json.loads(self.fileService.read(configVarMap.get(symbols)))
            else:  # Symbols value is a single symbol
                symbols = [symbols]
            config.update({'symbols': symbols})

        return config
