from factory import db
from models.blockchain import BlockchainDocument


# Function to add seed data to the database


def get_blockchain_rows():
    return db.session.query(BlockchainDocument).all()


def count_blockchain_content():
    return db.session.query(BlockchainDocument.content).all()


def fetch_blockchain_by_metadata():
    return db.session.query(BlockchainDocument.blockchain_metadata).all()


def fetch_blockchain_source_type():
    return db.session.query(BlockchainDocument.source_url).all()


# def fetch_specific_records():
#     return db.session.query(Project.coingecko_id).all()


# def fetch_filtered_records():
#     return db.session.query(URL.url_type).all()
