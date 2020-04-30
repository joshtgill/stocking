from forms.query_form import QueryForm
from services.file_service import FileService


class QueryService:

    def __init__(self, configInterface, queryInterface):
        self.configInterface = configInterface
        self.queryInterface = queryInterface

        self.queryForms = self.configInterface.get('queries', QueryForm)


    def start(self):
        for queryForm in self.queryForms:
            results = self.queryInterface.query(queryForm)

            resultsStr = ''
            for row in results:
                resultsStr += '{}\n'.format(row)

            fileService = FileService('data/{}_{}_to_{}_{}.txt'.format(queryForm.symbol,
                                                                       queryForm.start.strftime(self.configInterface.get('dateFormat')),
                                                                       queryForm.end.strftime(self.configInterface.get('dateFormat')),
                                                                       queryForm.interval))
            fileService.write(resultsStr)
