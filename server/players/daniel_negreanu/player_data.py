import os
import requests

from pprint import pprint
from dotenv import load_dotenv

from googleapiclient.discovery import build




load_dotenv()


def get_negreanu_pdfs():
  return [
    "players/daniel_negreanu/daniel_pdfs/class_guide.pdf",
    "players/daniel_negreanu/daniel_pdfs/DN_Fundamentals.pdf",
    

  ]
vlogs = "PL3N4X2Kgtefd0TBjVFEHWdJeU-ozIk5Iy"

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
# video_urls = get_playlist_videos(vlogs, api_key)
# for url in video_urls:
#     print(url)