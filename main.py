import sys
sys.path.append('query/')
from query.query_service import QueryService


QUERY_CONFIG_FILE_PATH = 'config/query_config.json'

if __name__ == "__main__":
    QueryService(QUERY_CONFIG_FILE_PATH).start()
