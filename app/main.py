import openai
import config
from telebot import TeleBot

# Your OpenAI API Key
openai.api_key = config.openai_api_key

# Your Telegram bot token
bot = TeleBot(config.bot_token)


# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, config.start_message)


# Define a function to handle all other messages
@bot.message_handler(func=lambda m: True)
def echo(message):
    text = message.text
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{text}",
        temperature=0.9,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response_text = response.choices[0].text
    if message.from_user.id == config.admin_id:
        bot.send_message(message.chat.id, response_text)
    else:
        bot.forward_message(config.admin_id, message.chat.id, message.id)
        bot.send_message(config.admin_id, response_text)
        bot.send_message(message.chat.id, response_text)


# Start the bot
print("Bot Started!")
bot.polling()
