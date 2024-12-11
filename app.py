import requests
import os

# Chemin vers le fichier contenant les clés API
API_KEYS_FILE = "MusicAutomationApp/privacy/API_key.txt"


# Charger les clés API depuis le fichier
def load_api_keys(file_path):
    keys = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                keys[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Erreur: le fichier {file_path} est introuvable.")
    return keys


api_keys = load_api_keys(API_KEYS_FILE)
SOUNDCLOUD_ACCESS_TOKEN = api_keys.get("SOUNDCLOUD_ACCESS_TOKEN")
YOUTUBE_ACCESS_TOKEN = api_keys.get("YOUTUBE_ACCESS_TOKEN")
TIKTOK_ACCESS_TOKEN = api_keys.get("TIKTOK_ACCESS_TOKEN")


# Fonction pour uploader sur SoundCloud
def upload_to_soundcloud(file_path, title, description):
    url = "https://api.soundcloud.com/tracks"
    headers = {
        "Authorization": f"OAuth {SOUNDCLOUD_ACCESS_TOKEN}"
    }
    data = {
        "track[title]": title,
        "track[description]": description,
        "track[sharing]": "public",
    }
    with open(file_path, "rb") as file:
        files = {
            "track[asset_data]": file
        }
        response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code == 201:
        print("Upload sur SoundCloud réussi!")
    else:
        print(f"Erreur SoundCloud: {response.status_code} - {response.text}")


# Fonction pour uploader sur YouTube
def upload_to_youtube(file_path, title, description):
    url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    headers = {
        "Authorization": f"Bearer {YOUTUBE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["music", "AI", "video"],
            "categoryId": "10"  # Catégorie Musique
        },
        "status": {
            "privacyStatus": "public"
        }
    }
    # Initialiser l'upload
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        upload_url = response.headers.get("Location")
        with open(file_path, "rb") as file:
            video_response = requests.put(upload_url, headers={"Authorization": f"Bearer {YOUTUBE_ACCESS_TOKEN}"},
                                          data=file)
            if video_response.status_code == 200:
                print("Upload sur YouTube réussi!")
            else:
                print(f"Erreur YouTube: {video_response.status_code} - {video_response.text}")
    else:
        print(f"Erreur initiale YouTube: {response.status_code} - {response.text}")


# Fonction pour uploader sur TikTok
def upload_to_tiktok(file_path, title, description):
    url = "https://open-api.tiktok.com/share/video/upload/"
    headers = {
        "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}"
    }
    data = {
        "title": title,
        "description": description
    }
    with open(file_path, "rb") as file:
        files = {
            "video": file
        }
        response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code == 200:
        print("Upload sur TikTok réussi!")
    else:
        print(f"Erreur TikTok: {response.status_code} - {response.text}")


# Exemple d'utilisation
def main():
    file_path = "votre_video.mp4"  # Chemin vers votre fichier vidéo
    title = "Ma Vidéo Générée par IA"
    description = "Cette vidéo a été générée automatiquement avec AI."

    if os.path.exists(file_path):
        print("Début de l'upload sur toutes les plateformes...")
        upload_to_soundcloud(file_path, title, description)
        upload_to_youtube(file_path, title, description)
        upload_to_tiktok(file_path, title, description)
    else:
        print("Le fichier vidéo spécifié n'existe pas.")


if __name__ == "__main__":
    main()
