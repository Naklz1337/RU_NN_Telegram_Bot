import logging
import NN
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token='')
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
	answer = NN.response(message.text)
	print(message.text,'|', answer)
	await message.answer(answer)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)