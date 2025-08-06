# ---------------------------------------------------------------------------------
# Name: SpotifyNow
# Description: Автообновление био с текущим треком Spotify (для Linux/Windows)
# Author: @YourNickname
# Commands: .spotifyon, .spotifyoff
# ---------------------------------------------------------------------------------

import os
import asyncio
from telethon.tl.functions.account import UpdateProfileRequest
from .. import loader, utils

try:
    from dbus import SessionBus  # Для Linux
    BUS_AVAILABLE = True
except ImportError:
    BUS_AVAILABLE = False  # Для Windows

class SpotifyNowMod(loader.Module):
    strings = {"name": "SpotifyNow"}

    def __init__(self):
        self.running = False

    async def client_ready(self, client, db):
        self.client = client

    # Для Linux (KDE/GNOME)
    def get_spotify_linux(self):
        if not BUS_AVAILABLE:
            return None
        try:
            bus = SessionBus()
            spotify = bus.get_object(
                "org.mpris.MediaPlayer2.spotify",
                "/org/mpris/MediaPlayer2"
            )
            metadata = spotify.Get(
                "org.mpris.MediaPlayer2.Player",
                "Metadata",
                dbus_interface="org.freedesktop.DBus.Properties"
            )
            return f"{', '.join(metadata['xesam:artist'])} - {metadata['xesam:title']}"
        except Exception as e:
            print(f"DBus error: {e}")
            return None

    # Для Windows
    def get_spotify_windows(self):
        try:
            import requests
            r = requests.get("http://localhost:4380/remote/status.json", timeout=2)
            data = r.json()
            if data.get("track") and data.get("playing"):
                artist = data["track"]["artist"][0]["name"]
                title = data["track"]["name"]
                return f"{artist} - {title}"
        except:
            return None

    async def update_bio(self):
        while self.running:
            track = None
            if os.name == "posix":  # Linux/MacOS
                track = self.get_spotify_linux()
            else:  # Windows
                track = self.get_spotify_windows()

            if track:
                await self.client(UpdateProfileRequest(about=f"🎧 {track}"))
            await asyncio.sleep(10)  # Проверка каждые 10 сек

    @loader.command(alias="spotifyon")
    async def spotifyon(self, message):
        """Включить автообновление био"""
        if self.running:
            await utils.answer(message, "🔄 Уже работает!")
            return

        self.running = True
        asyncio.create_task(self.update_bio())
        await utils.answer(message, "✅ Автообновление био включено!")

    @loader.command(alias="spotifyoff")
    async def spotifyoff(self, message):
        """Выключить автообновление"""
        if not self.running:
            await utils.answer(message, "❌ Уже выключено!")
            return

        self.running = False
        await self.client(UpdateProfileRequest(about=""))
        await utils.answer(message, "❌ Автообновление био отключено!")
