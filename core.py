import requests
from config import whitelist
from utils import send_log
from database import save_query_log

def analyze_article(bot, message):
    art = message.text.strip()
    user_id = str(message.chat.id)
    send_log(user_id, art)
    save_query_log(user_id, art)

    base_url = f"https://alm-basket-cdn-02.geobasket.ru/vol{art[0:4]}/part{art[0:6]}/{art}"

    # --- Информация о товаре ---
    info_url = f"{base_url}/info/ru/card.json"
    resp = requests.get(info_url)
    if resp.status_code == 200:
        data = resp.json()
        bot.send_message(message.chat.id, f"📦 {data.get('imt_name', 'Название недоступно')}")
        bot.send_message(message.chat.id, f"🔢 Артикул: {data.get('imt_id', '-')}")
        bot.send_message(message.chat.id, f"🎨 Цвет: {data.get('nm_colors_names', '-')}")
        bot.send_message(message.chat.id, f"📝 Описание: {data.get('description', '-')}")
        bot.send_message(message.chat.id, f"📂 Тип: {data.get('subj_name', '-')}")
        bot.send_message(message.chat.id, f"🏷 Бренд: {data.get('selling', {}).get('brand_name', '-')}")
    else:
        bot.send_message(message.chat.id, "❌ Ошибка загрузки информации о товаре")

    # --- История цен ---
    price_url = f"{base_url}/info/price-history.json"
    resp2 = requests.get(price_url)
    if resp2.status_code == 200:
        try:
            data2 = resp2.json()
            prices = [round(item['price']['RUB'] * 6.4 / 100) for item in data2 if 'RUB' in item['price']]
            if prices:
                current = prices[-1]
                avg = sum(prices) / len(prices)
                level = "Цена ниже средней" if current < avg else "Цена выше средней" if current > avg else "Цена равна средней"
                bot.send_message(message.chat.id, f"💰 Средняя цена: {round(avg)}₸\n💸 Текущая цена: {current}₸\n📉 Уровень цены: {level}")
            else:
                bot.send_message(message.chat.id, "⚠️ Пустая история цен")
        except:
            bot.send_message(message.chat.id, "⚠️ Ошибка при разборе истории цен")
    else:
        bot.send_message(message.chat.id, "❌ Не удалось получить историю цен")

    # --- Рейтинг и количество отзывов ---
    details_url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=kzt&dest=269&spp=30&nm={art}"
    resp3 = requests.get(details_url)
    if resp3.status_code == 200:
        try:
            product = resp3.json()['data']['products'][0]
            rating = product.get('reviewRating', 'N/A')
            feedbacks = product.get('feedbacks', 'N/A')
            bot.send_message(message.chat.id, f"📊 Рейтинг: {rating} ⭐\n💬 Отзывов: {feedbacks}")
        except:
            bot.send_message(message.chat.id, "⚠️ Не удалось получить рейтинг")
    else:
        bot.send_message(message.chat.id, "❌ Рейтинг не получен")

    # --- Отзывы (вопросы/ответы) ---
    imt_id = data.get('imt_id')
    if imt_id:
        q_url = f"https://questions.wildberries.ru/api/v1/questions?imtId={imt_id}&take=3&skip=0"
        q_resp = requests.get(q_url)
        if q_resp.status_code == 200:
            try:
                questions = q_resp.json().get('questions', [])
                if questions:
                    msgs = ["🗣 Последние отзывы:"]
                    for q in questions:
                        text = q.get('text', '')
                        answer = q.get('answer', {}).get('text', '')
                        msgs.append(f"❓ {text}\n💬 {answer if answer else 'Без ответа'}")
                    bot.send_message(message.chat.id, "\n\n".join(msgs))
                else:
                    bot.send_message(message.chat.id, "Нет отзывов")
            except:
                bot.send_message(message.chat.id, "⚠ Ошибка получения отзывов")