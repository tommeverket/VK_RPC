import time
import vk_api
from pypresence import Presence
import sys
from datetime import datetime
import requests
import urllib.parse
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io

class MusicTracker:
    def __init__(self, config):
        self.config = config
        self.last_track = None
        self.track_start_time = time.time()
        self.last_artwork_url = None
        self.rpc_connected = False
        self.root = None
        self.frame1 = None
        self.frame2 = None
        
    def connect_vk(self):
        """Подключение к VK API"""
        try:
            self.vk_session = vk_api.VkApi(token=self.config['vk_token'])
            self.vk = self.vk_session.get_api()
            user_info = self.vk.users.get()
            self.user_name = f"{user_info[0]['first_name']} {user_info[0]['last_name']}"
            return True
        except Exception as e:
            print(f"Ошибка подключения к VK: {e}")
            return False
    
    def connect_discord(self):
        """Подключение к Discord RPC"""
        try:
            self.RPC = Presence(self.config['discord_client_id'])
            self.RPC.connect()
            self.rpc_connected = True
            return True
        except Exception as e:
            print(f"Ошибка подключения к Discord: {e}")
            return False
    
    def update_discord_presence(self, artist, title, duration=0):
        """Обновление Discord Rich Presence"""
        try:
            # Подготавливаем данные для RPC
            rpc_data = {
                'details': title[:128],
                'state': artist[:128],
                'large_image': 'music',
                'large_text': f"{artist} - {title}"[:128]
            }
            
            # Добавляем кнопки
            if self.config['show_buttons']:
                rpc_data['buttons'] = [{"label": "VK Музыка", "url": "https://vk.com/music"}]
            
            # Используем обложку, если нашли
            if self.config['search_artwork'] and self.last_artwork_url:
                rpc_data['large_image'] = self.last_artwork_url
            
            self.RPC.update(**rpc_data)
            
        except Exception as e:
            print(f"Ошибка Discord RPC: {e}")
    
    def clear_presence(self):
        """Очистка Discord статуса"""
        try:
            if self.rpc_connected:
                self.RPC.clear()
                print(f"Статус очищен")
        except:
            pass

def search_apple_music_artwork(artist, title):
    """Поиск обложки через Apple Music API"""
    try:
        query = f"{artist} {title}"
        encoded_query = urllib.parse.quote(query)
        url = f"https://itunes.apple.com/search?term={encoded_query}&media=music&limit=1"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('resultCount', 0) > 0:
                track = data['results'][0]
                artwork_url = track.get('artworkUrl100', '')
                if artwork_url:
                    high_res_url = artwork_url.replace('100x100bb', '512x512bb').replace('100x100', '512x512')
                    return high_res_url
        return None
    except Exception as e:
        print(f"Ошибка поиска обложки: {e}")
        return None

def get_current_track(vk):
    """Получение текущего трека"""
    try:
        status = vk.status.get()
        
        if 'audio' in status and status['audio']:
            audio = status['audio']
            
            # Если audio - словарь (один трек)
            if isinstance(audio, dict):
                track = audio
                if 'artist' in track and 'title' in track:
                    return {
                        'artist': track['artist'],
                        'title': track['title'],
                        'duration': track.get('duration', 0)
                    }
            
            # Если audio - список (несколько треков)
            elif isinstance(audio, list) and len(audio) > 0:
                track = audio[0]
                if isinstance(track, dict) and 'artist' in track and 'title' in track:
                    return {
                        'artist': track['artist'],
                        'title': track['title'],
                        'duration': track.get('duration', 0)
                    }
        
        # Проверяем поле 'text' как резервный вариант
        if 'text' in status and status['text']:
            text = status['text']
            if ' — ' in text:
                parts = text.split(' — ', 1)
                if len(parts) == 2:
                    return {
                        'artist': parts[0].strip(),
                        'title': parts[1].strip(),
                        'duration': 0
                    }
            elif ' - ' in text:
                parts = text.split(' - ', 1)
                if len(parts) == 2:
                    return {
                        'artist': parts[0].strip(),
                        'title': parts[1].strip(),
                        'duration': 0
                    }
                    
    except Exception as e:
        print(f"Ошибка получения трека: {e}")
    
    return None

class VKMusicRPCApp:
    def __init__(self):
        self.tracker = None
        self.running = False
        self.paused = False
        self.no_track_count = 0  # Счетчик отсутствия треков
        self.setup_gui()
        
    def setup_gui(self):
        """Настройка GUI интерфейса"""
        self.root = tk.Tk()
        self.root.title("VK Music Discord RPC")
        self.root.geometry("600x400")
        self.root.configure(bg='#1f1f1f')
        self.root.resizable(False, False)
        
        # Создаем фреймы
        self.create_frames()
        
        # Скрываем второй фрейм изначально
        self.frame2.grid_remove()
        
        # Запускаем проверку
        self.check_connection()
        
    def create_frames(self):
        """Создание двух фреймов"""
        # Frame 1 - успешное подключение
        self.frame1 = tk.Frame(self.root, bg='#333333', width=580, height=380)
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Заголовок
        self.header_label = tk.Label(
            self.frame1, 
            text="Logged In as User Name", 
            font=("Arial", 10), 
            bg='#333333', 
            fg='white'
        )
        self.header_label.place(x=10, y=10)
        
        # Обложка
        self.cover_frame = tk.Frame(self.frame1, bg='#444444', width=120, height=120)
        self.cover_frame.place(x=10, y=30)
        self.cover_label = tk.Label(
            self.cover_frame, 
            text="🎵", 
            bg='#444444', 
            fg='white', 
            font=("Arial", 48),
            justify='center'
        )
        self.cover_label.pack(expand=True, fill='both')
        
        # Название и исполнитель
        self.title_label = tk.Label(
            self.frame1, 
            text="Title", 
            font=("Arial", 20, "bold"), 
            bg='#333333', 
            fg='white',
            wraplength=420,
            justify='left'
        )
        self.title_label.place(x=140, y=30)
        
        self.artist_label = tk.Label(
            self.frame1, 
            text="Artist", 
            font=("Arial", 16), 
            bg='#333333', 
            fg='white',
            wraplength=420,
            justify='left'
        )
        self.artist_label.place(x=140, y=80)
        
        # Статус
        self.status_label = tk.Label(
            self.frame1, 
            text="Discord RPC is running!", 
            font=("Arial", 10), 
            bg='#333333', 
            fg='green'
        )
        self.status_label.place(x=140, y=120)
        
        # Подсказка
        self.hint_label = tk.Label(
            self.frame1, 
            text="", 
            font=("Arial", 9), 
            bg='#333333', 
            fg='orange',
            wraplength=400,
            justify='left'
        )
        self.hint_label.place(x=140, y=140)
        
        # Кнопка паузы
        self.pause_button = tk.Button(
            self.frame1, 
            text="Pause", 
            command=self.toggle_pause, 
            bg='#ff9900', 
            fg='white', 
            font=("Arial", 10, "bold"),
            width=10
        )
        self.pause_button.place(x=500, y=350)
        
        # Frame 2 - ошибка
        self.frame2 = tk.Frame(self.root, bg='#333333', width=580, height=380)
        self.frame2.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Текст ошибки
        self.error_label = tk.Label(
            self.frame2, 
            text="Error! You're not logged in!\nCheck config.json !", 
            font=("Arial", 16), 
            bg='#333333', 
            fg='white',
            justify='center'
        )
        self.error_label.place(relx=0.5, rely=0.4, anchor='center')
        
        # Кнопка паузы для ошибки
        self.pause_button2 = tk.Button(
            self.frame2, 
            text="Pause", 
            command=self.toggle_pause, 
            bg='#ff9900', 
            fg='white', 
            font=("Arial", 10, "bold"),
            width=10
        )
        self.pause_button2.place(relx=0.5, rely=0.6, anchor='center')
        
    def truncate_text(self, text, max_length):
        """Обрезка текста с добавлением ..."""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def adjust_font_size(self, text, base_size, max_chars):
        """Настройка размера шрифта под длину текста"""
        if len(text) <= max_chars:
            return base_size
        reduction = (len(text) - max_chars) // 4
        return max(10, base_size - reduction)
    
    def check_connection(self):
        """Проверка подключения"""
        # Загружаем конфигурацию
        config = load_config()
        if config is None:
            self.show_error()
            return
            
        if config['vk_token'] == "ВСТАВЬТЕ_СЮДА_ВАШ_ТОКЕН_ВК":
            self.show_error()
            return
            
        if config['discord_client_id'] == "ВАШ_DISCORD_APP_CLIENT_ID":
            self.show_error()
            return
            
        # Создаем трекер
        self.tracker = MusicTracker(config)
        
        # Попытка подключиться
        if self.tracker.connect_vk():
            if self.tracker.connect_discord():
                self.show_success()
                self.start_tracking()
            else:
                self.show_error()
        else:
            self.show_error()
    
    def show_success(self):
        """Показать успешное подключение"""
        self.frame2.grid_remove()
        self.frame1.grid()
        
        # Обновляем информацию о пользователе
        user_display = self.truncate_text(f"Logged In as {self.tracker.user_name}", 40)
        self.header_label.config(text=user_display)
        
        # Устанавливаем дефолтную обложку
        self.set_default_image()
        
        # Обновляем статус
        self.status_label.config(text="Discord RPC is running!", fg='green')
        self.hint_label.config(text="")  # Скрываем подсказку
        
    def show_error(self):
        """Показать ошибку"""
        self.frame1.grid_remove()
        self.frame2.grid()
        
        # Обновляем статус
        self.status_label.config(text="Error connecting to services", fg='red')
        
    def set_default_image(self):
        """Установить дефолтную обложку - принудительный сброс"""
        try:
            print("Сброс обложки на дефолтную")
            # Принудительно удаляем изображение и устанавливаем символ ноты
            self.cover_label.config(image="", text="🎵", font=("Arial", 48))
            # Удаляем сохраненную ссылку на изображение
            if hasattr(self.cover_label, 'image'):
                delattr(self.cover_label, 'image')
        except Exception as e:
            print(f"Ошибка сброса обложки: {e}")
            try:
                # Резервный способ
                self.cover_label.config(text="🎵", font=("Arial", 48))
            except:
                pass
    
    def show_hint(self):
        """Показать подсказку о включении стриминга"""
        hint_text = "💡 Подсказка: Включите 'Транслировать в статус' в настройках VK Музыки"
        self.hint_label.config(text=hint_text)
        
    def hide_hint(self):
        """Скрыть подсказку"""
        self.hint_label.config(text="")
    
    def toggle_pause(self):
        """Переключение паузы"""
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume")
            self.pause_button2.config(text="Resume")
            self.status_label.config(text="Discord RPC is paused", fg='orange')
            # Очищаем Discord статус
            if self.tracker:
                self.tracker.clear_presence()
            # Сбрасываем счетчик
            self.no_track_count = 0
            self.hide_hint()
        else:
            self.pause_button.config(text="Pause")
            self.pause_button2.config(text="Pause")
            self.status_label.config(text="Discord RPC is running!", fg='green')
            # Возобновляем отслеживание
            if self.running:
                self.check_track()
    
    def start_tracking(self):
        """Запуск отслеживания"""
        self.running = True
        self.no_track_count = 0  # Сброс счетчика при запуске
        self.check_track()
        
    def check_track(self):
        """Проверка текущего трека"""
        if not self.running or self.paused:
            return
            
        try:
            track_info = get_current_track(self.tracker.vk)
            
            if track_info:
                artist = track_info['artist']
                title = track_info['title']
                
                current_track = (artist, title)
                
                # Проверяем смену трека
                if current_track != self.tracker.last_track:
                    # Новый трек!
                    print(f"Новый трек: {artist} - {title}")
                    self.tracker.last_track = current_track
                    self.tracker.last_artwork_url = None  # Сброс обложки для нового поиска
                    
                    # Обрезаем длинные строки
                    title_display = self.truncate_text(title, 50)
                    artist_display = self.truncate_text(artist, 40)
                    
                    # Настройка размера шрифта
                    title_size = self.adjust_font_size(title, 20, 35)
                    artist_size = self.adjust_font_size(artist, 16, 30)
                    
                    # Обновляем UI
                    self.title_label.config(
                        text=title_display,
                        font=("Arial", title_size, "bold")
                    )
                    self.artist_label.config(
                        text=artist_display,
                        font=("Arial", artist_size)
                    )
                    
                    # Ищем обложку для нового трека
                    if self.tracker.config['search_artwork']:
                        print("Поиск обложки...")
                        artwork_url = search_apple_music_artwork(artist, title)
                        if artwork_url:
                            print("Обложка найдена")
                            self.tracker.last_artwork_url = artwork_url
                            self.load_image_from_url(artwork_url)
                        else:
                            print("Обложка не найдена")
                            self.set_default_image()
                    else:
                        self.set_default_image()
                    
                    # Обновляем Discord RPC
                    self.tracker.update_discord_presence(artist, title)
                    
                    # Сбрасываем счетчик и скрываем подсказку
                    self.no_track_count = 0
                    self.hide_hint()
                    
                else:
                    # Тот же трек, просто обновляем RPC если нужно
                    self.tracker.update_discord_presence(artist, title)
                    # Сбрасываем счетчик
                    self.no_track_count = 0
                    self.hide_hint()
                
            else:
                # Если музыка не играет
                self.no_track_count += 1
                print(f"Трек не найден. Счетчик: {self.no_track_count}")
                
                # Показываем подсказку после 3-х последовательных проверок без трека
                if self.no_track_count >= 3:
                    self.show_hint()
                
                # Если трек был, то очищаем
                if self.tracker.last_track is not None:
                    print("Музыка остановлена - сброс обложки")
                    self.clear_display()
                    self.tracker.clear_presence()
                    self.tracker.last_track = None
                    self.tracker.last_artwork_url = None
                    # Принудительный сброс обложки
                    self.root.after(100, self.set_default_image)
                    # Сбрасываем счетчик
                    self.no_track_count = 0
                    self.hide_hint()
                    
        except Exception as e:
            print(f"Ошибка проверки трека: {e}")
        
        # Повторяем проверку
        self.root.after(2000, self.check_track)  # Проверка каждые 2 секунды
    
    def clear_display(self):
        """Очистка дисплея"""
        self.title_label.config(
            text="Title", 
            font=("Arial", 20, "bold")
        )
        self.artist_label.config(
            text="Artist", 
            font=("Arial", 16)
        )
        # Принудительный сброс обложки
        self.set_default_image()
        
    def load_image_from_url(self, url):
        """Загрузка изображения по URL"""
        try:
            print(f"Загрузка обложки: {url}")
            response = requests.get(url, timeout=5)
            img = Image.open(io.BytesIO(response.content))
            # Ресайз до нужного размера
            img = img.resize((120, 120), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            # Принудительно удаляем текст и устанавливаем изображение
            self.cover_label.config(image=photo, text="")
            self.cover_label.image = photo  # Сохраняем ссылку
            print("Обложка успешно загружена")
            # Скрываем подсказку при успешной загрузке
            self.hide_hint()
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.set_default_image()
    
    def on_close(self):
        """Обработчик закрытия"""
        self.running = False
        if self.tracker:
            self.tracker.clear_presence()
            try:
                self.tracker.RPC.close()
            except:
                pass
        self.root.destroy()
        sys.exit()

def load_config():
    """Загрузка конфигурации из файла"""
    config_file = 'config.json'
    
    # Стандартная конфигурация
    default_config = {
        "vk_token": "ВСТАВЬТЕ_СЮДА_ВАШ_ТОКЕН_ВК",
        "discord_client_id": "ВАШ_DISCORD_APP_CLIENT_ID",
        "check_interval": 2,
        "search_artwork": True,
        "use_apple_music": True,
        "show_buttons": True,
        "debug_mode": False
    }
    
    # Если файл не существует, создаем его
    if not os.path.exists(config_file):
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        return default_config
    
    # Загружаем конфигурацию
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Проверяем наличие всех необходимых полей
        for key in default_config:
            if key not in config:
                config[key] = default_config[key]
        
        return config
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        return None

if __name__ == "__main__":
    app = VKMusicRPCApp()
    # Обработчик закрытия окна
    app.root.protocol("WM_DELETE_WINDOW", app.on_close)
    app.root.mainloop()