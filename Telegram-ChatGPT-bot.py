import telethon 
from telethon.tl.custom import Button
from telethon import TelegramClient, events

import asyncio 
import config 
import openai 



openai.api_key = config.openai_key


client = TelegramClient(config.session_name_bot, config.API_ID, config.API_HASH).start(bot_token=config.BOT_TOKEN)



keyboard_stop = [[Button.inline("Stop and reset conversation", b"stop")]]



async def send_question_and_retrieve_result(prompt, conv, keyboard):
    """
    Sends a question to the user and retrieves their response.

    Args:
        prompt (str): The question to ask the user.
        conv (telethon.client.conversations.Conversation): The conversation object to use for sending the message.
        keyboard (list): The keyboard to send with the message.

    Returns:
        Tuple[Union[events.callbackquery.CallbackQuery.Event, str], telethon.types.Message]: A tuple containing the user's response and the message object.
    """
    
    message = await conv.send_message(prompt, buttons = keyboard)
    
    loop = asyncio.get_event_loop()
    
    task1 = loop.create_task(
        conv.wait_event(events.CallbackQuery())
    )
    task2 = loop.create_task(
        conv.get_response()
    )

    done, _ = await asyncio.wait({task1, task2}, return_when=asyncio.FIRST_COMPLETED)
    
    result = done.pop().result()
    await message.delete()
    
    if isinstance(result, events.CallbackQuery.Event):
        return None
    else:
        return result.message.strip()


@client.on(events.NewMessage(pattern="(?i)/start"))
async def handle_start_command(event):
    """
    Starts a new conversation with the user.

    Args:
        event (telethon.events.NewMessage): The event that triggered this function.
    """

    SENDER = event.sender_id
    prompt = "Hello 🤖! I'm Telegram-ChatGPT-Bot, an AI-powered Telegram chatbot ready to assist you with any question you have. Simply ask me anything, and I'll provide you with an answer using advanced language models and machine learning algorithms."
    try:
        await client.send_message(SENDER, prompt)

        async with client.conversation(await event.get_chat(), exclusive=True, timeout=600) as conv:
            history = []

            while True:
                prompt = "Please provide your input to Telegram-ChatGPT-Bot"
                user_input = await send_question_and_retrieve_result(prompt, conv, keyboard_stop)
                
                if user_input is None:
                    prompt = "Received. Conversation will be reset. Type /start to start a new one!"
                    await client.send_message(SENDER, prompt)
                    break
                else:
                    prompt = "Received! I'm thinking about the response..."
                    thinking_message = await client.send_message(SENDER, prompt)

                    history.append({"role":"user", "content": user_input})

                    chat_completion = openai.ChatCompletion.create(
                        model=config.model_engine, # ID of the model to use.
                        messages=history, # The messages to generate chat completions for. This must be a list of dicts!
                        max_tokens=500, # The maximum number of tokens to generate in the completion.
                        n=1, # How many completions to generate for each prompt.
                        temperature=0.1 # Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
                    )

                    response = chat_completion.choices[0].message.content 

                    history.append({"role": "assistant", "content": response})

                    await thinking_message.delete()
                    
                    await client.send_message(SENDER, response, parse_mode='Markdown')


    except asyncio.TimeoutError:
        await client.send_message(SENDER, "<b>Conversation ended✔️</b>\nIt's been too long since your last response. Please type /start to begin a new conversation.", parse_mode='html')
        return

    except telethon.errors.common.AlreadyInConversationError:
        pass

    except Exception as e: 
        print(e)
        await client.send_message(SENDER, "<b>Conversation ended✔️</b>\nSomething went wrong. Please type /start to begin a new conversation.", parse_mode='html')
        return


if __name__ == "__main__":
    print("Bot Started...")    
    client.run_until_disconnected() 


