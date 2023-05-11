from Google import Create_Service
from googleapiclient.http import MediaFileUpload

def upload_video(white, black, opening, eco_code):
  CLIENT_SECRET_FILE = 'youtube/client_secret.json'
  API_NAME = 'youtube'
  API_VERSION = 'v3'
  SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

  service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

  request_body = {
      'snippet': {
          'categoryI': 20,
          'title': f"{white} vs {black}",
          'description': f"Chess game between {white} and {black}.\n\n{eco_code} {opening}\n\n\nSong:\n––––––––––––––––––––––––––––––\nWe Are One by Vexento https://soundcloud.com/vexento\nhttps://www.youtube.com/user/Vexento\nFree Download / Stream: http://bit.ly/2PaIKcR\nMusic promoted by Audio Library https://youtu.be/Ssvu2yncgWU\n––––––––––––––––––––––––––––––",
          'tags': ["chess", "titled players", "chess game", eco_code, opening]
      },
      'status': {
          'privacyStatus': 'public',
          'selfDeclaredMadeForKids': False, 
      },
      'notifySubscribers': True
  }

  mediaFile = MediaFileUpload('result.mp4')

  response_upload = service.videos().insert(
      part='snippet,status',
      body=request_body,
      media_body=mediaFile
  ).execute()


  service.thumbnails().set(
      videoId=response_upload.get('id'),
      media_body=MediaFileUpload('data/thumbnails/thumbnail.jpg')
  ).execute()