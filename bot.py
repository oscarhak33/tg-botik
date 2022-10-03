import config
import logging

from aiogram import Bot,  Dispatcher, executor, types

from filters import IsAdminFilter

#log level
logging.basicConfig(level=logging.INFO)

#bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение пользователя!")
        return

    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply("Пользоватаель был забанен!")

@dp.message_handler(content_types=["new_chat_members"])
async def on_user_joined(message: types.Message):
    await message.delete()

@dp.message_handler()
async def filter_message(message: types.Message):
    if "Сука" in message.text:
        await message.delete()

if  __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)