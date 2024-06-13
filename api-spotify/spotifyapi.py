import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configurações de autenticação do Spotify
SPOTIPY_CLIENT_ID = '3db89f83884a4015b46a151806f2bd63'
SPOTIPY_CLIENT_SECRET = '8a1b9422601a4a2183e39834aef24f22'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback/'

scope = 'user-library-read playlist-read-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))


# Função para obter playlists do usuário
def get_user_playlists():
    playlists = sp.current_user_playlists(limit=50)
    all_playlists = []
    
    while playlists:
        for playlist in playlists['items']:
            all_playlists.append(playlist)
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    
    return all_playlists

# Função para obter faixas de uma playlist
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks

# Função para exportar playlists para um arquivo JSON
def export_playlists_to_json():
    playlists = get_user_playlists()
    exported_data = []
    quantidade_de_playlist = 0
    for playlist in playlists:
        tracks = get_playlist_tracks(playlist['id'])
        track_list = []
        
        quantidade_de_playlist = quantidade_de_playlist + 1

        quantidade_musicas = 0
        for item in tracks:
            track = item['track']
            #print( track['name'])
            if track is not None:
                quantidade_musicas = quantidade_musicas + 1
                track_list.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name']
                })
        
        exported_data.append({
            'playlist_name': playlist['name'],
            'tracks': track_list
        })
        print(f'Playlist n: {quantidade_de_playlist} | Quantidade de musica na playlist: {quantidade_musicas} ')
    with open('spotify_playlists.json', 'w', encoding='utf-8') as f:
        json.dump(exported_data, f, ensure_ascii=False, indent=4)



# Executa a exportação
export_playlists_to_json()
print("Exportação concluída! O arquivo spotify_playlists.json foi criado.")
