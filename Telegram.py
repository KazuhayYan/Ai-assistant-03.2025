from ML_SDK import ask_gpt
import telebot
from Configuration import HOME_DIR, COUNT_LAST_MSG
from Database import add_message, select_n_last_messages
from Limits import *
from creds import get_bot_token

bot = telebot.TeleBot(get_bot_token())

@bot.message_handler(commands=['start]'])
def start_handler(message):
    bot.send_message(message.from_user.id,"Привет! Я бот-собеседник с которым ты можешь поговорить, что-нибудь спросить, рассказать о своих переживаниях и тому подобное")
    bot.send_message(message.from_user.id, "Если нужна помощь отправь комнаду /help")

@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.from_user.id, 'Использовать бота очень просто!\n'
                                           'Отправь текстовое сообщение и в ответ получишь текст от YandexGPT Lite, а если ты отправишь голосовое сообщение,'
                                           ' то в ответ тоже получишь голосовое сообщение!')

@bot.message_handler(commands=['debug'])
def debug_handler(message):
    with open(f'{HOME_DIR}/logs.txt', 'r') as s:
        bot.send_document(message.chat.id, s)

@bot.message_handler(func=lambda message: message.content_type==["text"])
def text_handler(message):
    try:
        user_id = message.from_user.id
        status_check_users, error_message = check_number_of_users(user_id)
        if not status_check_users:
            bot.send_message(user_id, error_message)
            return
        full_user_message = [message.text, 'user', 0, 0, 0]
        add_message(user_id=user_id, full_message=full_user_message)
        last_messages, total_spent_tokens = select_n_last_messages(user_id, COUNT_LAST_MSG)
        total_gpt_tokens, error_message = is_gpt_token_limit(last_messages, total_spent_tokens)
        if error_message:
            bot.send_message(user_id, error_message)
            return
        status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)
        if not status_gpt:
            bot.send_message(user_id, answer_gpt)
            return
        total_gpt_tokens += tokens_in_answer
        full_gpt_message = [answer_gpt, 'assistant', total_gpt_tokens, 0, 0]
        add_message(user_id=user_id, full_message=full_gpt_message)
        bot.send_message(user_id, answer_gpt, reply_to_message_id=message.id)
    except Exception as e:
        logging.error(e)
        bot.send_message(message.from_user.id, "Не получилось ответить. Попробуй написать другое сообщение")

bot.infinity_polling()
