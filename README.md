# TON ↔ RUB Converter Bot

Простой бот для конвертации Toncoin в российские рубли и обратно. Использует [python-telegram-bot](https://python-telegram-bot.org/) и данные CoinGecko.

## Установка

1. Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
source venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Скопируйте `.env.example` в `.env` и впишите токен бота.

4. Запустите бота:

```bash
python bot.py
```
