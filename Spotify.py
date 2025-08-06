# ---------------------------------------------------------------------------------
# Name: SpotifyNowPlaying
# Description: Автообновление био с текущим треком из Spotify (Arch Linux + KDE)
# Author: @YourNickname
# Commands: .spotifybio / .spotifyoff
# ---------------------------------------------------------------------------------

__version__ = (1, 0, 0)

import asyncio
import os
from telethon.tl.functions.account import UpdateProfileRequest
from .. import loader, utils
from dbus import SessionBus  # На Arch Linux это работает!

@loader.tds
class SpotifyNowPlayingMod(loader.Module):
    """Автообновление био с текущим треком (Spotify + KDE Plasma)"""

    strings = {
        "name": "SpotifyNowPlaying",
        "on": "🎧 <b>Автообновление био включено!</b>",
        "off": "🎧 <b>Автообновление био выключено.</b>",
        "error": "❌ <b>Ошибка: Spotify не запущен или трек не найден.</b>",
    }

    def __init__(self):
        self.running = False
        self.me = None

    async def client_ready(self, client, db):
        self.client = client
        self.me = await client.get_me()

    def get_spotify_track(self):
        """Получает текущий трек через DBUS (KDE Plasma)"""
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
            artist = ", ".join(metadata["xesam:artist"])
            title = metadata["xesam:title"]
            return f"{artist} - {title}"
        except Exception as e:
            print(f"DBUS error: {e}")
            return None

    async def update_bio_loop(self):
        """Цикл обновления био"""
        while self.running:
            track = self.get_spotify_track()
            if track:
                await self.client(UpdateProfileRequest(about=f"🎧 {track}"))
            await asyncio.sleep(10)  # Проверка каждые 10 сек

    @loader.command(ru_doc="Включить автообновление био")
    async def spotifybio(self, message):
        """Включить автообновление"""
        if self.running:
            await utils.answer(message, self.strings["on"])
            return

        # Проверяем, запущен ли Spotify
        track = self.get_spotify_track()
        if not track:
            await utils.answer(message, self.strings["error"])
            return

        self.running = True
        asyncio.create_task(self.update_bio_loop())
        await utils.answer(message, self.strings["on"])

    @loader.command(ru_doc="Выключить автообновление био")
    async def spotifyoff(self, message):
        """Выключить автообновление"""
        if not self.running:
            await utils.answer(message, self.strings["off"])
            return

        self.running = False
        await self.client(UpdateProfileRequest(about=""))
        await utils.answer(message, self.strings["off"])
