import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# Variables globales
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE = "MusicAutomationApp/privacy/client_secret_youtube.json"

def authenticate_youtube():
    # Authentification OAuth
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

#
def upload_video(youtube, file_path, title, description):
    # Préparation des métadonnées
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["AI", "music", "video"],
            "categoryId": "10"  # Catégorie Musique
        },
        "status": {
            "privacyStatus": "public"  # Rend la vidéo publique
        }
    }

    # Chargement du fichier vidéo
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    # Upload de la vidéo
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    response = request.execute()
    print("Upload réussi. ID de la vidéo :", response.get("id"))

def main():
    file_path = "votre_video.mp4"  # Chemin de votre vidéo
    title = "Ma Vidéo Générée par IA"
    description = "Cette vidéo a été générée automatiquement avec AI."

    if not os.path.exists(file_path):
        print(f"Erreur : le fichier {file_path} n'existe pas.")
        return

    youtube = authenticate_youtube()
    upload_video(youtube, file_path, title, description)

if __name__ == "__main__":
    main()
