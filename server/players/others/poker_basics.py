import os
import requests

from pprint import pprint
from dotenv import load_dotenv

from googleapiclient.discovery import build

load_dotenv()

def get_poker_pdfs():
  return [
    "players/others/theory_of_poker.pdf",
  ]