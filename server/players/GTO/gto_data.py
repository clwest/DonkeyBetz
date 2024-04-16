import os
import requests

from pprint import pprint
from dotenv import load_dotenv

from googleapiclient.discovery import build

def get_gto_pdfs():
  return [
    "players/GTO/gto_pdfs/exploitability_and_gto.pdf",
    "players/GTO/gto_pdfs/gto_strategies.pdf",
    "players/GTO/gto_pdfs/search_for_gto.pdf",
  ]

gto_videos = "PLV0Rs5uYPfcuS684PJFinDdkg4P91r8qp"

def get_playlist_videos(playlist_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    video_urls = []
    next_page_token = None

    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,  # API allows max 50 items per request
            pageToken=next_page_token
        )

        pl_response = pl_request.execute()

        video_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]
        video_urls.extend([f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids])

        next_page_token = pl_response.get('nextPageToken')

        if not next_page_token:
            break

    return video_urls

# Example usage
# playlist_id = get_playlist_videos()  # Replace with your playlist ID
# api_key = os.getenv("YOUTUBE_API_KEY")
# video_urls = get_playlist_videos(strategies_id, api_key)
# for url in video_urls:
#     print(url)