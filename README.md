# **Telegram ChatGPT Bot**

Check the video explanation here: https://youtu.be/ERGUgZqkrkk

This code provides a Python implementation of a Telegram Chatbot based on the OpenAI GPT-3 model. This bot uses the Telethon Python library to interact with the Telegram Bot API and the OpenAI API to generate responses to user queries.

## **Installation**

1. Clone the repository and navigate to the project directory:
    
```
git clone https://github.com/yourusername/Telegram-ChatGPT-bot.git
cd Telegram-ChatGPT-bot
```
    
2. Install the required packages:
    
```
pip install -r requirements.txt
```
    

## **Configuration**

The bot requires an OpenAI API key and Telegram Bot API credentials to function. You must create a **`config.py`** file in the same directory as the **`bot.py`** file and include the following variables:

- **`openai_key`**: Your OpenAI API key
- **`API_ID`**: Your Telegram API ID
- **`API_HASH`**: Your Telegram API hash
- **`BOT_TOKEN`**: Your Telegram bot token
- **`session_name_bot`**: A name for the Telegram client session

You can obtain a Telegram API ID and hash by following the instructions **[here](https://core.telegram.org/api/obtaining_api_id)**. To obtain a bot token, you can talk to **[BotFather](https://telegram.me/botfather)** on Telegram. To obtain the OpenAi key go **[here](https://platform.openai.com/account/api-keys)**.

## **Usage**

To start the bot, run the following command in your terminal:

```
python Telegram-ChatGPT-bot.py
```

This will start the bot and wait for user queries. Once the bot is running, you can interact with it by sending messages to it in Telegram.

The bot will respond to any message it receives by generating a response using the OpenAI API and sending it back to the user. The bot will continue generating responses until the conversation times out or the user clicks the "Stop and reset conversation" button.
