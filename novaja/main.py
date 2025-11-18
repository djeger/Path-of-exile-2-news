import telebot
import requests
from telebot import types
from config import token

bot = telebot.TeleBot(token)

def get_poe2_news():
    try:
        url = 'https://www.reddit.com/r/pathofexile/search.json'

        params = {
            'q': 'path of exile 2',
            'sort': 'new',
            'limit': 5
        }
        
        headers =  {'User-Agent': 'PoE2Bot/1.0'}

        response = requests.get(url)

        data = response.json()

        news_list = []
        for post in data['data']['children']:
            post_data = post['data']
            news_list.append({
                'title': post_data['title'],
                'link': f"https://www.reddit.com{post_data['permalink']}"
            })
        
        return news_list
    except:
        return [] 


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.InlineKeyboardButton('Новости', callback_data='news')
    btn2 = types.InlineKeyboardButton('Официальный сайт', callback_data='official')
    btn3 = types.InlineKeyboardButton('Помощь', callback_data='help')
    btn4 = types.InlineKeyboardButton('Reddit', callback_data="reddit")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f'Привет, я бот, который тебе расскажет про новости про poe 2 \n\n'
        f'Выбери действие на клавиатуре',
        reply_markup = main_menu()
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        '❓ <b>Справка по боту</b>\n\n'
        '<b>Команды:</b>\n'
        '/start - Главное меню\n'
        '/news - Последние новости\n'
        '/help - Эта справка\n\n'
        '<b>Кнопки:</b>\n'
        '📰 Новости - Последние обсуждения на Reddit\n'
        '🎮 Официальный сайт - Ссылка на pathofexile.com\n'
        '💬 Reddit - Ссылка на сообщество\n'
        '❓ Помощь - Эта справка'
    )
    bot.send_message(message.chat.id, help_text, parse_mode='HTML')

@bot.message_handler(commands=['news'])
def news(message):
    show_news(message)

def show_news(message):
    """Показывает новости"""
    loading = bot.send_message(message.chat.id, '⏳ Загружаю новости...')
    
    print("Вызвана функция show_news()")  # 🔍 Отладка
    
    news = get_poe2_news()
    
    print(f"Получено новостей: {len(news) if news else 0}")  # 🔍 Отладка
    
    if not news:
        bot.edit_message_text(
            '❌ Не удалось загрузить новости.\n\n'
            'Попробуй позже или перейди на сайт',
            message.chat.id,
            loading.message_id
        )
        
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('🌐 Перейти на сайт', url='https://www.pathofexile.com/pathofexile2')
        markup.add(btn)
        bot.send_message(message.chat.id, 'Нажми на кнопку ниже:', reply_markup=markup)
        return
    
    # Формируем текст
    news_text = '📰 <b>Последние новости Path of Exile 2:</b>\n\n'
    
    for i, item in enumerate(news, 1):
        news_text += f'{i}. <a href="{item["link"]}">{item["title"]}</a>\n\n'
    
    print(f"Текст новостей готов, длина: {len(news_text)}")  # 🔍 Отладка
    
    try:
        bot.delete_message(message.chat.id, loading.message_id)
    except:
        pass  # Игнорируем ошибку удаления
    
    bot.send_message(
        message.chat.id,
        news_text,
        parse_mode='HTML',
        disable_web_page_preview=True
    )
    
    print("Новости отправлены!")  # 🔍 Отладка
# Обработка нажатий на кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'Новости':
        show_news(message)

    elif message.text == 'Официальный сайт':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('🌐 Официальный сайт', url='https://www.pathofexile.com/pathofexile2')
        btn2 = types.InlineKeyboardButton('📺 YouTube канал', url='https://www.youtube.com/c/pathofexile')
        markup.add(btn1)
        markup.add(btn2)

        bot.send_message(
        '🎮 <b>Path of Exile 2</b>\n\n'
        'Выбери ссылку:',
        parse_mode='HTML',
        reply_markup=markup
    )

    elif message.text == 'Reddit':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Reddit PoE2', url='https://www.reddit.com/r/PathOfExile2/')
        btn2 = types.InlineKeyboardButton('Reddit PoE', url='https://www.reddit.com/r/pathofexile/')
        markup.add(btn1)
        markup.add(btn2)
        
        bot.send_message(
            message.chat.id,
            '💬 <b>Сообщество Reddit</b>\n\n'
            'Выбери сабреддит:',
            parse_mode='HTML',
            reply_markup=markup
        )
    
    elif message.text == 'Помощь':
        help_text = (
            '❓<b>Справка по боту</b>\n\n'
            '<b>Кнопки:</b>\n'
            '📰 Новости - Последние обсуждения\n'
            '🎮 Официальный сайт - Ссылки на сайт и YouTube\n'
            '💬 Reddit - Ссылки на сообщества\n'
            '❓ Помощь - Эта справка\n\n'
            '<b>Команды:</b>\n'
            '/start - Главное меню\n'
            '/news - Показать новости\n'
            '/help - Справка'
        )
        bot.send_message(message.chat.id, help_text, parse_mode='HTML')
    
    else:
        bot.send_message(
            message.chat.id,
            '🤔 Не понимаю эту команду.\n'
            'Используй кнопки на клавиатуре или команду /help'
        )

if __name__ == '__main__':
    print('Бот запущен')
    bot.polling(none_stop=True)