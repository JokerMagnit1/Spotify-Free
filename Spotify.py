import os
import asyncio
import subprocess
from telethon.tl.functions.account import UpdateProfileRequest
from .. import loader, utils

class SpotifyBioMod(loader.Module):
    strings = {"name": "SpotifyBio"}

    def __init__(self):
        self.running = False

    async def client_ready(self, client, db):
        self.client = client
        self._db = db

    async def update_bio(self):
        while self.running:
            try:
                # Универсальный метод через playerctl
                track = subprocess.getoutput(
                    "playerctl -p spotify metadata --format '{{artist}} - {{title}}' 2>/dev/null"
                )
                
                if track and "No player found" not in track:
                    print(f"[Spotify] Updating bio: {track}")
                    await self.client(UpdateProfileRequest(about=f"🎧 {track}"))
                else:
                    print("[Spotify] No active track")
                    
                await asyncio.sleep(15)
            except Exception as e:
                print(f"[Spotify Error] {e}")
                await asyncio.sleep(30)

    @loader.command()
    async def spotifyon(self, message):
        """Включить автообновление био"""
        if self.running:
            await utils.answer(message, "🔄 Уже включено!")
            return
            
        self.running = True
        asyncio.create_task(self.update_bio())
        await utils.answer(message, "✅ Автообновление био включено!")

    @loader.command()
    async def spotifyoff(self, message):
        """Выключить автообновление"""
        if not self.running:
            await utils.answer(message, "🔄 Уже выключено!")
            return
            
        self.running = False
        await utils.answer(message, "❌ Автообновление био отключено")
