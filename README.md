# Бот-викторина "Тотемное животное" для Московского зоопарка

Telegram-бот, который помогает пользователям определить их тотемное животное и рассказывает о программе опеки над животными в Московском зоопарке.

## Установка и запуск

1. **Клонируйте репозиторий**:
```bash
git clone https://github.com/yourusername/totem-animal-bot.git
cd totem-animal-bot
```

2. **Установите зависимости**:
```bash
python3 -m venv venv
 ./venv/bin/pip3 install -r requirements.txt
```

3. **Настройте конфигурационный файл**:

Укажите ваш BOT_TOKEN (токен полученный от @BotFather), а также SHARE_URL (адрес вашего бота)

4. **Запустите бота**:
```bash
./venv/bin/python3 main.py
 ```

5. **Остановить бота**:
```bash
pkill -f "python.*main.py"
```
