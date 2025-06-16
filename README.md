# 🤖 Wildberries Product Analyzer Bot

Телеграм-бот на Python, который по артикулу товара с Wildberries показывает:
- 📌 название
- 💵 цену
- ⭐️ рейтинг
- 💬 количество отзывов
- ❓ до 3 отзывов (вопросов)
- 🔒 доступ только по whitelist
- 🧾 логирует и сохраняет в базу данных SQLite

---

## 🚀 Функции

- ✅ Поиск товара по артикулу
- ✅ Защита доступа (whitelist)
- ✅ Логирование всех запросов (`log.txt`)
- ✅ Сохранение запросов в SQLite (`bot_data.db`)
- ✅ Парсинг отзывов с WB API
- ✅ Поддержка `pytest`-тестов

---

## 🛠 Установка и запуск

### 1. Клонируй проект

```bash
git clone https://github.com/your-username/wb-analyzer-bot.git
cd wb-analyzer-bot
