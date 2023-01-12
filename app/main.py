import openai
import telebot
import config

# Your OpenAI API Key
openai.api_key = config.openai_api_key

# Your Telegram bot token
bot = telebot.TeleBot(config.bot_token)


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
        temperature=0.5,
        max_tokens=100
    )
    response_text = response.choices[0].text
    bot.send_message(message.chat.id, response_text)


# Start the bot
print("Bot Started!")
bot.polling()
