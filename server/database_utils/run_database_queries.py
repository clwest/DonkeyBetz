from database_utils.database_queries import *
from factory import create_app
from pprint import pprint

app = create_app()

with app.app_context():
    print("***Blockchain Count***")
    pprint(count_blockchain_content())
    print("***Source Type***")
    pprint(fetch_blockchain_source_type())

    print("***Blockchain Name***")
    pprint(fetch_blockchain_by_metadata())
