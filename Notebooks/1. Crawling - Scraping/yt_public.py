import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from iteration_utilities import unique_everseen

# Import the modified process_comments and make_csv functions
from utils.youtube_comments import process_comments, make_csv

load_dotenv()
API_KEY = os.getenv("API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)

def comment_threads(videoId, to_csv=True):
    comments_list = []

    # Fetch comments using YouTube API
    request = youtube.commentThreads().list(
        part='id,snippet',
        videoId=videoId,
    )
    response = request.execute()
    comments_list.extend(process_comments(response['items'], csv_output=False))

    # Continue fetching comments if nextPageToken exists
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,snippet',
            videoId=videoId,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))

    # Remove duplicates from comments_list
    comments_list = list(unique_everseen(comments_list))

    print(f"Finished fetching comments for {videoId}. {len(comments_list)} comments found.")

    # Save comments to CSV file if to_csv is True
    if to_csv:
        make_csv(comments_list, videoId)

    return comments_list

if __name__ == '__main__':
    videoId = 'yiffzzl7EFY'
    response = comment_threads(videoId)
    print(response)
