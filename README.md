# 🎵 VK Music Discord RPC

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)](https://github.com/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/)
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
[![vk_api](https://img.shields.io/badge/using-vk_api-00bb88.svg?style=for-the-badge&logo=vk&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

🎵 Программа для отображения текущей играющей песни из VK в Discord Rich Presence с графическим интерфейсом

[![VK Music RPC Demo](https://img.shields.io/badge/view-screenshots-blue)](https://github.com/python273/vk_api)

## 📖 Содержание
- [Описание](#описание)
- [Особенности](#особенности)
- [Скриншоты](#скриншоты)
- [Установка](#установка)
- [Конфигурация](#конфигурация)
- [Использование](#использование)
- [Решение проблем](#решение-проблем)
- [Лицензия](#лицензия)

## 📋 Описание

VK Music Discord RPC - это приложение, которое позволяет автоматически отображать информацию о текущей играющей песне из VKонтакте в статусе Discord. Программа отслеживает вашу музыку в реальном времени и обновляет Discord Rich Presence с названием песни, исполнителем и обложкой.

## 🌟 Особенности

- ✅ Отслеживание текущей песни в VK в реальном времени
- 🎨 Автоматический поиск и отображение обложек через Apple Music API
- 🖼️ Графический интерфейс с отображением информации о треке
- ⏸️ Возможность остановить показ трека в RPC
- 🔧 Простая настройка через конфигурационный файл
- 🔄 Мгновенная реакция на смену треков

## 📸 Скриншоты

<div align="center">
  <img src="https://img.shields.io/badge/screenshot-success_screen-blue" alt="Успешное подключение" width="45%"/>
  <img src="https://img.shields.io/badge/screenshot-error_screen-red" alt="Ошибка подключения" width="45%"/>
</div>

*Успешное подключение и отображение ошибок*

## 📦 Установка

### Требования:
- Python 3.7 или выше
- Установленный Discord (должен быть запущен)

### Установка зависимостей:
~~~bash
pip install vk_api pypresence pillow requests
~~~

### Клонирование репозитория:
~~~bash
git clone https://github.com/ваш_логин/vk-music-discord-rpc.git
cd vk-music-discord-rpc
~~~

## ⚙️ Конфигурация

При первом запуске программа создаст файл `config.json` со следующими параметрами:

~~~json
{
    "vk_token": "ВСТАВЬТЕ_СЮДА_ВАШ_ТОКЕН_ВК",
    "discord_client_id": "ВАШ_DISCORD_APP_CLIENT_ID",
    "check_interval": 2,
    "search_artwork": true,
    "use_apple_music": true,
    "show_buttons": true,
    "debug_mode": false
}
~~~

### Получение токена VK:
1. Перейдите по ссылке (замените `APP_ID`):
   ~~~
   https://oauth.vk.com/authorize?client_id=APP_ID&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,audio,status,wall,offline&response_type=token&v=5.131
   ~~~
2. Разрешите доступ
3. Скопируйте токен из адресной строки

### Создание Discord Application:
1. Перейдите на [Discord Developer Portal](https://discord.com/developers/applications)
2. Нажмите "New Application"
3. Введите название (например, "VK Music RPC")
4. Скопируйте "Application ID"

## ▶️ Использование

### Запуск из исходного кода:
```bash
python main.py
```

### Использование программы:
1. Запустите программу
2. Убедитесь, что Discord запущен
3. Включите музыку в VK (включите "Транслировать в статус")
4. Программа автоматически обнаружит трек
5. Используйте кнопку "Pause/Resume" для управления

## 🎯 Создание EXE

## ❓ Решение проблем

### "Error! You're not logged in!":
- ✅ Проверьте правильность токена VK в config.json
- ✅ Убедитесь, что токен не истек

### Обложка не отображается:
- Проверьте подключение к интернету
- Убедитесь, что параметр `search_artwork` установлен в `true`
- Убедитесь, что автор и название песни совпадают с данными Apple

### Discord RPC не работает:
- ✅ Убедитесь, что Discord запущен
- ✅ Проверьте правильность Discord Client ID
- ✅ Перезапустите Discord

### Музыка не обнаружена:
- ✅ Включите "Транслировать в статус" в настройках VK Музыки
- ✅ Убедитесь, что музыка реально играет

### Ошибки при создании EXE:
~~~bash
# Используйте параметр --hidden-import
pyinstaller --onefile --windowed --hidden-import=PIL._tkinter_finder main.py
~~~

## 🛠️ Разработка

### Структура проекта:
~~~
vk-music-rpc/
├── main.py          # Основной код
├── config.json      # Файл конфигурации
├── README.md        # Документация
├── LICENSE          # Лицензия
├── requirements.txt # Зависимости
└── screenshots/     # Скриншоты
~~~

## 🤝 Поддержка

Если у вас возникли проблемы с установкой или использованием программы:

1. Создайте [Issue](https://github.com/username/repo/issues) в репозитории
2. Опишите проблему подробно
3. Приложите скриншоты ошибок
4. Укажите вашу ОС и версию Python

## 📄 Лицензия

MIT License - вы можете свободно использовать, изменять и распространять эту программу.

Смотрите файл [LICENSE](LICENSE) для подробной информации.

## 🙏 Благодарности

- [vk_api](https://github.com/python273/vk_api) - для работы с API VK
- [pypresence](https://github.com/qwertyquerty/pypresence) - для Discord RPC
- [Pillow](https://github.com/python-pillow/Pillow) - для работы с изображениями
- Создано с помощью искусственного интеллекта 🤖

## 🚀 Поддержка проекта

Если вам понравился проект:
- ⭐ Поставьте звезду на GitHub
- 🐛 Сообщайте о багах
- 💡 Предлагайте улучшения
- 📢 Расскажите друзьям

---

<div align="center">
  <sub>Создано с ❤️ для сообщества VK и Discord</sub>
</div>

[Вверх ⬆️](#vk-music-discord-rpc)
