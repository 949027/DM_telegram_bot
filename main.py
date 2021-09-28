import logging
import os
import time
import telegram

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from dotenv import load_dotenv

import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# TOKEN = '2009911477:AAE3ZP3tGYdx4OqZqWZTvyX56x1XdnqanRQ'
# TOKEN = '2022344697:AAFjDURv67Rmw_QGvEw4XHifm8LlmT8vmQo'  # test
TOKEN = '2010821521:AAHquG-HTFBWN15KSLjNCGs7dcmD83gLjt4'
bot = telegram.Bot(token=TOKEN)

CHECK_INPUT, DOWNLOAD_PHOTO, GET_TITLE, GET_CATEGORY1, GET_CATEGORY2, CHOOSE_CATEGORY1, CHOOSE_CATEGORY2 = range(7)

reply_keyboard = [['Добавить вещь', 'Найти вещь', 'Обменяться']]
reply_keyboard_start = [['Добавить вещь', 'Найти вещь']]
reply_keyboard_category1 = [
    ['одежда, обувь', 'аксессуары, украшения', 'кухонная утварь'],
    ['бытовая техника', 'продукты питания'],
    ['игрушки и детские вещи', 'детская одежда и обувь'],
    ['ремонт и строительство', 'ещё'],
]

reply_keyboard_category2 = [['назад', 'спортивные вещи'],
                            ['мебель, интерьерные вещи', 'коллекционные вещи'],
                            ['электроника', 'творчества и хобби'],
                            ['транспорт', 'растения', 'другое'],
                            ]

markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
markup_start = ReplyKeyboardMarkup(reply_keyboard_start, resize_keyboard=True,
                                   one_time_keyboard=True)
markup_category1 = ReplyKeyboardMarkup(reply_keyboard_category1,
                                       resize_keyboard=True,
                                       one_time_keyboard=True)
markup_category2 = ReplyKeyboardMarkup(reply_keyboard_category2,
                                       resize_keyboard=True,
                                       one_time_keyboard=True)



def start(update, context):
    time.sleep(1)
    user = update.message.from_user
    user_id = user.id
    text = f'Привет {user.first_name}! Я помогу тебе обменять что-то ненужное на очень нужное. Чтобы разместить вещь к обмену напиши - “Добавить вещь”. После этого тебе станут доступны вещи других пользователей. Напиши “Найти вещь” и я пришлю тебе фотографии вещей для обмена. Понравилась вещь - пиши “Обменяться”, нет - снова набирай “Найти вещь”. Если кому-то понравится предложенная тобой вещь, то я пришлю тебе контакты владельца.'
    update.message.reply_text(text)
    time.sleep(1)

    if db.get_one_thing(user_id) == None:
        update.message.reply_text(
            'Вы - новый пользователь. Для начала работы необходимо добавить хотя бы одну вещь')
        time.sleep(1)
        update.message.reply_text('Пожалуйста пришли мне фотографию вещи.')
        return DOWNLOAD_PHOTO
    else:
        update.message.reply_text('Привет, выбери что-нибудь для обмена.',
                                  reply_markup=markup_start)
    return CHECK_INPUT


def download_photo(update, context):
    user = update.message.from_user
    directory = f'{user.first_name}_{user.id}'
    os.makedirs(directory, exist_ok=True)
    photo_id = update.message.photo[-1].file_id
    path = os.path.join(directory, photo_id)
    photo_file = update.message.photo[-1].get_file()
    db_path = f'{path}.jpg'
    context.user_data['db_path'] = db_path
    photo_file.download(db_path)
    logger.info(f"{user.username} added a photo")
    time.sleep(1)
    update.message.reply_text('Пожалуйста, напиши мне название этой вещи.')
    return GET_TITLE


def get_title(update, context):
    title = update.message.text
    context.user_data['title'] = title
    logger.info("Title: %s", update.message.text)
    time.sleep(1)
    update.message.reply_text('Выберите категорию',
                              reply_markup=markup_category1)
    return GET_CATEGORY1


def get_catigory1(update, context):
    catigory1 = ['одежда, обувь', 'аксессуары, украшения', 'кухонная утварь',
                 'бытовая техника', 'продукты питания',
                 'игрушки и детские вещи', 'детская одежда и обувь',
                 'ремонт и строительство'
                 ]
    logger.info("Category: %s", update.message.text)
    if update.message.text in catigory1:
        user = update.message.from_user
        user_id = user.id
        category = update.message.text
        chat_id = update.message.chat_id
        username = user.username
        db_path = context.user_data.get('db_path')
        title = context.user_data.get('title')
        db.add_thing(title, db_path, user_id, category, chat_id, username)
        update.message.reply_text('Ваша вещь принята)')
        time.sleep(1)
        update.message.reply_text(
            'Чтобы посмотреть доступные вещи напиши “Найти вещь”',
            reply_markup=markup_start)
        return CHECK_INPUT
    elif update.message.text == 'ещё':
        update.message.reply_text(
            'Выберите категорию', reply_markup=markup_category2)
        return GET_CATEGORY2


def get_catigory2(update, context):
    catigory2 = ['спортивные вещи', 'мебель, интерьерные вещи',
                 'коллекционные вещи',
                 'электроника', 'творчества и хобби', 'ремонт и строительство',
                 'транспорт', 'растения', 'другое'
                 ]
    logger.info("Category: %s", update.message.text)
    if update.message.text in catigory2:
        user = update.message.from_user
        user_id = user.id
        category = update.message.text
        chat_id = update.message.chat_id
        username = user.username
        db_path = context.user_data.get('db_path')
        title = context.user_data.get('title')
        db.add_thing(title, db_path, user_id, category, chat_id,
                     username)  # запись вещи в БД
        update.message.reply_text('Ваша вещь принята)')
        time.sleep(1)
        update.message.reply_text(
            'Чтобы посмотреть доступные вещи нажми “Найти вещь”',
            reply_markup=markup_start)
        return CHECK_INPUT
    elif update.message.text == 'назад':
        update.message.reply_text(
            'Выберите категорию', reply_markup=markup_category1)
        return GET_CATEGORY1


def check_input(update, context):
    user_message = update.message.text
    tg_chat_id = update.message.chat_id
    context.user_data['tg_chat_id'] = tg_chat_id
    time.sleep(1)
    if user_message == 'Добавить вещь':
        update.message.reply_text('Пожалуйста пришли мне фотографию вещи.',
                                  reply_markup=ReplyKeyboardRemove())
        return DOWNLOAD_PHOTO
    elif user_message == 'Найти вещь':
        update.message.reply_text('Выберите категорию',
                                  reply_markup=markup_category1)
        return CHOOSE_CATEGORY1
    elif user_message == 'Обменяться':
        exchange_things(update)
        update.message.reply_text('Принято, можешь продолжить выбор вещей')
    else:
        update.message.reply_text("Неверная команда.")
        return CHECK_INPUT
    logger.info("Button: ", update.message.text)


def exchange_things(update):
    user = update.message.from_user
    user_id = user.id
    id_owner = thing[3]
    id_owner1 = thing[3]
    id_thing = thing[0]
    db.add_priority_things(id_owner, user_id)
    db.add_thing_like(user_id, id_thing, id_owner1)
    if not db.check_for_matches(user_id, id_owner):
        update.message.reply_text('Вот контакты владельца данной вещи:')
        update.message.reply_text('@' + thing[6])
        message = 'Ранее этот пользователь интересовался твоей вещью: ' + \
                  db.get_thing(db.check_for_matches(user_id, id_owner)[1])[1]
        update.message.reply_text(message)
        message = 'Привет! Пользователь @' + user.username + ' заинтересовался твоей вещью: ' + \
                  thing[1] + '. Ранее вы интересовались его вещью: ' + (
                      db.get_thing(db.check_for_matches(user_id, id_owner)[1])[
                          1])
        bot.send_message(chat_id=id_owner, text=message)


def cancel(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
    )
    return ConversationHandler.END


def choose_catigory1(update, context):
    catigory1 = ['одежда, обувь', 'аксессуары, украшения',
                 'кухонная утварь',
                 'бытовая техника', 'продукты питания', 'все категории',
                 'игрушки и детские вещи', 'детская одежда и обувь',
                 'ремонт и строительство'
                 ]
    logger.info(f"choose_catigory: {update.message.text}")
    if update.message.text in catigory1:
        choose_category = update.message.text
        update.message.reply_text(f'Kатегория: "{choose_category}"',
                                  reply_markup=markup)
        send_pictures_to_telegram(update, context, choose_category)
        return CHECK_INPUT
    elif update.message.text == 'ещё':
        update.message.reply_text(
            'Выберите категорию', reply_markup=markup_category2)
        return CHOOSE_CATEGORY2


def choose_catigory2(update, context):
    catigory2 = ['спортивные вещи', 'мебель, интерьерные вещи',
                 'коллекционные вещи',
                 'электроника', 'творчества и хобби', 'ремонт и строительство',
                 'транспорт', 'растения', 'другое'
                 ]
    logger.info(f"choose_catigory: {update.message.text}")
    if update.message.text in catigory2:
        choose_category = update.message.text
        update.message.reply_text(f'Kатегория: "{choose_category}"',
                                  reply_markup=markup)
        send_pictures_to_telegram(update, choose_category)
        return CHECK_INPUT
    elif update.message.text == 'назад':
        update.message.reply_text(
            'Выберите категорию', reply_markup=markup_category1)
        return CHOOSE_CATEGORY1


def send_pictures_to_telegram(update, context, choose_category):
    user = update.message.from_user
    user_id = user.id
    id_thing = db.cut_priority_thing(user_id)
    tg_chat_id = context.user_data.get('tg_chat_id')
    if id_thing:
        global thing
        thing = db.get_thing(id_thing)
        name_thing = thing[1]
        path = thing[2]
        update.message.reply_text(
            'Обратите внимание, эта вещь пользователя которому нравится одна из Ваших вещей')
        with open(path, "rb") as file:
            bot.send_photo(chat_id=tg_chat_id,
                           photo=open(path, "rb"))
        update.message.reply_text(name_thing)
        time.sleep(1)
        update.message.reply_text('Если вещь понравилась, жми "Обменяться"')
    else:
        try:
            random_thing = db.get_random_thing(user_id,
                                               choose_category)
            thing = random_thing
            name_thing = random_thing[1]
            path = random_thing[2]
            with open(path, "rb") as file:
                bot.send_photo(chat_id=tg_chat_id,
                               photo=open(path, "rb"))
            update.message.reply_text(name_thing)
        except TypeError:
            update.message.reply_text('Упс, пусто(. Попробуй ещё раз.')


def main():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            CHECK_INPUT: [CommandHandler('start', start),
                          MessageHandler(Filters.text, check_input)],

            DOWNLOAD_PHOTO: [CommandHandler('start', start),
                             MessageHandler(Filters.photo, download_photo)],

            GET_TITLE: [CommandHandler('start', start),
                        MessageHandler(Filters.text, get_title)],

            GET_CATEGORY1: [CommandHandler('start', start),
                            MessageHandler(Filters.text, get_catigory1)],

            GET_CATEGORY2: [CommandHandler('start', start),
                            MessageHandler(Filters.text, get_catigory2)],

            CHOOSE_CATEGORY1: [CommandHandler('start', start),
                               MessageHandler(Filters.text, choose_catigory1)],

            CHOOSE_CATEGORY2: [CommandHandler('start', start),
                               MessageHandler(Filters.text, choose_catigory2)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
