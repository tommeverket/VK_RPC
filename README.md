# 🎵 VK Music Discord RPC

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)](https://github.com/tommeverket/VK_RPC/releases/tag/release)
![Version](https://img.shields.io/badge/version-1.0-blue)
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
[![vk_api](https://img.shields.io/badge/using-vk_api-00bb88.svg?style=for-the-badge&logo=vk&logoWidth=20)](https://github.com/python273/vk_api)

🎵 Программа для отображения текущей играющей песни из VK в Discord Rich Presence с GUI

[![VK Music RPC Demo](https://github.com/tommeverket/VK_RPC/blob/main/screenshots/GUI_preview_working_running.png)]

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

[![ss](https://img.shields.io/badge/view-screenshots-blue&logoWidth=60)](https://github.com/tommeverket/VK_RPC/tree/main/screenshots)

## 📦 Установка

### Требования:
- Python 3.7 или выше
- Установленный Discord (должен быть запущен)

### Установка зависимостей:
```bash
pip install -r requirements.txt
```

### Клонирование репозитория:
```bash
git clone https://github.com/tommverket/VK_RPC.git
cd VK_RPC
```

## ⚙️ Конфигурация

При первом запуске программа создаст файл `config.json` со следующими параметрами:

```json
{
    "vk_token": "ВСТАВЬТЕ_СЮДА_ВАШ_ТОКЕН_ВК",
    "discord_client_id": "ВАШ_DISCORD_APP_CLIENT_ID",
    "check_interval": 2,
    "search_artwork": true,
    "use_apple_music": true,
    "show_buttons": true,
    "debug_mode": false
}
```

### Получение токена VK:
1. Перейдите по [ссылке](https://oauth.vk.com/oauth/authorize?client_id=6121396&scope=1115144&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1&slogin_h=1c303149381fdfa4ab.b807112eee8a0f0a20&__q_hash=172f249acc3b5044585b64397c2acbb6)
(Или создайте свою ссылку через https://vkhost.github.io)
2. Разрешите доступ
3. Скопируйте токен из адресной строки (после access_token= и до &expires_in=)

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


## ❓ Решение проблем

### "Error! You're not logged in!":
[![err_notconfigured](https://github.com/tommeverket/VK_RPC/blob/main/screenshots/GUI_error_notconfigured.png)]
- ✅ Проверьте правильность токена VK в config.json
- ✅ Убедитесь, что токен не истек

### Обложка не отображается:
- ✅ Проверьте подключение к интернету
- ✅ Убедитесь, что параметр `search_artwork` установлен в `true`
- ✅ Убедитесь, что автор и название песни совпадают с данными Apple

### Discord RPC не работает:
- ✅ Убедитесь, что Discord запущен
- ✅ Проверьте правильность Discord Client ID
- ✅ Перезапустите Discord

### Музыка не обнаружена:
[![err_musicnotfound](https://github.com/tommeverket/VK_RPC/blob/main/screenshots/GUI_error_musicnotfound.png)]
- ✅ Включите "Транслировать в статус" в настройках VK Музыки
- ✅ Убедитесь, что музыка реально играет

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
- Создано с помощью [искусственного интеллекта Qwen](https://chat.qwen.ai)🤖

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
