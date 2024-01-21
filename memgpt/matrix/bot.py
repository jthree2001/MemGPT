import time
import os
import simplematrixbotlib as botlib
from typing import Union, Callable, Optional, Tuple
from memgpt.matrix.message_handler import MessageHandler

token = os.getenv("MATRIX_TOKEN")
# token = "Batbro10102!"
username = os.getenv("MATRIX_USER")
# username ="deka-alpha"
matrix_server = os.getenv("MATRIX_SERVER")
# matrix_server = "https://chat.batbro.us"

creds = botlib.Creds(matrix_server, username, token)
bot = botlib.Bot(creds)
PREFIX = '!'


@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot():
        obj = {
            "room": room,
            "message": message
        }
        thread = MessageHandler(obj)
        thread.start()

        while thread.is_alive():
            await bot.async_client.room_typing(room.room_id)
            time.sleep(.5)
        thread.join()

        for r in thread.response:
            if "assistant_message" in r:
                print("ASSISTANT:", r["assistant_message"])
                await bot.api.send_text_message(
                    room.room_id, r["assistant_message"]
                )
            elif "internal_monologue" in r:
                print("THOUGHTS:", r["internal_monologue"])
            elif "function_call" in r:
                print("FUNCTION CALL:", r["function_call"])
                
            elif "function_return" in r:
                print("FUNCTION RETURN:", r["function_return"])
                if r["function_return"] != "None":
                    await bot.api.send_markdown_message(
                        room_id=room.room_id,
                        message= r["function_return"],
                        msgtype="m.notice")
                

