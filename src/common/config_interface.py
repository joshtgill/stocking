import json


class ConfigInterface:

    def __init__(self, fileInterface):
        self.fileInterface = fileInterface


    def load(self, configPath, role = ''):
        config = json.loads(self.fileInterface.read(configPath))

        if role == 'query':
            # Load any query config vars
            configVarMap = {'ALL_SYMBOLS': 'data/symbols/all_symbols.json'}
            symbols = config.get('symbols')
            if not isinstance(symbols, list):
                if symbols in configVarMap.keys():  # Symbols value is config var
                    symbols = json.loads(self.fileInterface.read(configVarMap.get(symbols)))
                else:  # Symbols value is a single symbol
                    symbols = [symbols]
                config.update({'symbols': symbols})

        return config
