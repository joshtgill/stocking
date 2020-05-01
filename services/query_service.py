from forms.query_form import QueryForm
from services.file_service import FileService


class QueryService:

    def __init__(self, configInterface, queryInterface):
        self.configInterface = configInterface
        self.queryInterface = queryInterface

        self.queryForms = self.buildForms()


    def buildForms(self):
        queryForms = []
        for queryData in self.configInterface.get('queries'):
            if len(queryData.get('symbols')) > 1:
                for symbol in queryData.get('symbols'):
                    queryForm = QueryForm(queryData)
                    queryForm.symbol = symbol
                    queryForms.append(queryForm)
            else:
                queryForm = QueryForm(queryData)
                queryForms.append(queryForm)

        return queryForms


    def makeQuery(self):
        for queryForm in self.queryForms:
            results = self.queryInterface.query(queryForm)

            resultsStr = ''
            for row in results:
                resultsStr += '{}\n'.format(row)

            fileService = FileService('{}/{}_{}_to_{}_{}.txt'.format(self.configInterface.get('stockDataDirectory'),
                                                                     queryForm.symbol,
                                                                     queryForm.start.strftime(self.configInterface.get('dateFormat')),
                                                                     queryForm.end.strftime(self.configInterface.get('dateFormat')),
                                                                     queryForm.interval))
            fileService.write(resultsStr)
