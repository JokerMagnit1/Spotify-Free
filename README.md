# Spotify-Free
# 🎧 SpotifyNowPlaying for Hikka

**Автоматическое обновление био в Telegram с текущим треком из Spotify**  
*(Работает без Spotify Premium, только локальный клиент)*  

![Demo](https://i.imgur.com/JQ6f3O2.gif)  
*(Пример работы модуля)*  

## 🔥 Возможности
- Отслеживает текущий трек **без Spotify API** (через DBUS/MPRIS2)  
- Автоматически обновляет био в Telegram  
- Поддержка **KDE Plasma (Arch Linux)** и **Windows**  
- Простые команды включения/выключения  

## ⚙️ Установка
### 1. Установите зависимости
#### Для Arch Linux:
```bash
sudo pacman -S playerctl python-dbus
