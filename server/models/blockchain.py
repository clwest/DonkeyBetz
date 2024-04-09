# from datetime import datetime
# import uuid
# from factory import db
# from enum import Enum
# from sqlalchemy import (
#     String,
#     Integer,
#     DateTime,
#     ForeignKey,
#     Text,
#     Boolean,
#     Table,
# )
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from sqlalchemy.dialects.postgresql import ARRAY
# from sqlalchemy import Column, Enum as SQLAlchemyEnum
# from sqlalchemy.types import TypeDecorator, BINARY


# class ContentType(Enum):
#     ARTICLE = "Article"
#     VIDEO = "Video"
#     DOCUMENTS = "Documents"
#     REPO = "Repo"


# class Blockchain(db.Model):
#     __tablename__ = "blockchains"

#     id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = db.Column(String(100), nullable=False, unique=True)
#     collection_name = db.Column(
#         String(255), unique=True
#     )  # Unique collection name for PGVector
#     symbol = db.Column(String(25))
#     image = db.Column(Text)
#     categories = db.Column(
#         String(50)
#     )  # e.g., 'Layer1', 'Infrastructure', 'Layer2', etc.
#     hashing_algorithm = db.Column(String(100), nullable=True)
#     description = db.Column(Text)
#     homepage = db.Column(Text, nullable=True)
#     blockchain_site = db.Column(Text, nullable=True)
#     chat_url = db.Column(Text, nullable=True)
#     twitter_name = db.Column(String(50), nullable=True)
#     country_origin = db.Column(String(50))
#     genesis_date = db.Column(DateTime)
#     block_time_in_minutes = db.Column(DateTime)
#     market_cap_rank = db.Column(Integer)
#     total_btc_locked = db.Column(Integer, nullable=True)
#     total_usd_locked = db.Column(db.BigInteger, nullable=True)
#     all_time_high = db.Column(Integer, nullable=True)
#     all_time_high_date = db.Column(DateTime, nullable=True)
#     all_time_low = db.Column(Integer, nullable=True)
#     all_time_low_date = db.Column(DateTime, nullable=True)

#     created_at = db.Column(DateTime, server_default=func.now())
#     updated_at = db.Column(DateTime, server_default=func.now(), onupdate=func.now())

#     def __init__(
#         self,
#         name,
#         collection_name,
#         symbol,
#         image,
#         categories,
#         hashing_algorithm,
#         description,
#         homepage,
#         blockchain_site,
#         twitter_name,
#         country_origin,
#         genesis_date,
#         block_time_in_minutes,
#         total_btc_locked,
#         total_usd_locked,
#         all_time_high,
#         all_time_high_date,
#         all_time_low,
#         all_time_low_date,
#     ):
#         self.name = name
#         self.collection_name = collection_name
#         self.symbol = symbol
#         self.image = image
#         self.categories = categories
#         self.hashing_algorithm = hashing_algorithm
#         self.description = description
#         self.homepage = homepage
#         self.blockchain_site = blockchain_site
#         self.twitter_name = twitter_name
#         self.country_origin = country_origin
#         self.genesis_date = genesis_date
#         self.block_time_in_minutes = block_time_in_minutes
#         self.total_btc_locked = total_btc_locked
#         self.total_usd_locked = total_usd_locked
#         self.all_time_high = all_time_high
#         self.all_time_high_date = all_time_high_date
#         self.all_time_low = all_time_low
#         self.all_time_low_date = all_time_low_date


# class BlockchainContent(db.Model):
#     __tablename__ = "blockchain_content"

#     id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     blockchain_id = db.Column(String(36), ForeignKey("blockchains.id"))
#     type = db.Column(
#         SQLAlchemyEnum(ContentType)
#     )  # Emum: Article, Video, Documents, etc.
#     title = db.Column(String(255))
#     url = db.Column(String(255))
#     content = db.Column(Text)
#     created_at = db.Column(DateTime, server_default=func.now())

#     blockchain = relationship("Blockchain", backref="contents")

#     def __init__(self, blockchain_id, type, title, url, content):
#         self.blockchain_id = blockchain_id
#         self.type = type
#         self.title = title
#         self.url = url
#         self.content = content


# class BlockchainRepo(db.Model):
#     __tablename__ = "blockchain_repos"
#     id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     blockchain_id = db.Column(String(36), ForeignKey("blockchains.id"))
#     name = db.Column(String(255))
#     repo_url = db.Column(String(255))
#     description = db.Column(Text)
#     created_at = db.Column(DateTime, server_defualt=func.now())

#     blockchain = relationship("Blockchain", backref="repositories")


# class DefiProject(db.Model):
#     __tablename__ = "defi_projects"
#     id = db.Column(Integer, primary_key=True)
#     blockchain_id = db.Column(String(35), ForeignKey("blockchains.id"))
#     name = db.Column(String(255), nullable=False)
#     description = db.Column(Text)
#     contract_address = db.Column(String())
#     liquidity_pools = db.Column(Text)
#     staking_details = db.Column(Text)
#     audit_info = db.Column(Text)
#     governance = db.Column(Text)

#     blockchain = relationship("Blockchain", backref="defi_project", lazy=True)
