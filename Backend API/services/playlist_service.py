from database.Database import Database
import services.song_service as song_service
from model.Playlist import Playlist
from model.Song import Song
from fastapi import HTTPException
from services.utils import checkValidParameterString
import json

playlistCollection = Database().connection["playlist"]


def get_playlist(name: str) -> Playlist:

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    playlist_data = playlistCollection.find_one({'name': name})

    if playlist_data is None:
        raise HTTPException(
            status_code=404, detail="La playlist con ese nombre no existe")

    playlist_songs = []

    [playlist_songs.append(song_service.get_song(song_name))
     for song_name in playlist_data["song_names"]]

    #[print(song.name) for song in playlist_songs]

    playlist = Playlist(name, playlist_data["photo"], playlist_songs)

    return playlist


def create_playlist(name: str, photo: str, song_names: list):

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    songs = song_service.get_songs(song_names)
    playlist = Playlist(name=name, photo=photo, songs=songs)

    result_playlist_exists = playlistCollection.find_one({'name': name})

    if result_playlist_exists:
        raise HTTPException(status_code=400, detail="La playlist ya existe")

    result = playlistCollection.insert_one(
        {'name': name, 'photo': photo, 'song_names': song_names})

    return True if result.acknowledged else False


def update_playlist(name: str, photo: str, song_names: list):

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_playlist_exists = playlistCollection.find_one({'name': name})

    if not result_playlist_exists:
        raise HTTPException(status_code=404, detail="La playlist no existe")

    playlistCollection.update_one({'name': name}, {
                                  "$set": {'name': name, 'photo': photo, 'song_names': song_names}})
