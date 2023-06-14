from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import subprocess

import asyncio

loop = asyncio.get_event_loop()

chat_id = -1

TOKEN = ""

USERID = ""

try:
    f = open("token.txt", "r")
    # print(f.read())
    TOKEN = str(f.read())
    print(repr(TOKEN))
except FileNotFoundError:
    pass

try:
    f = open("userid.txt", "r")
    # print(f.read())
    USERID = int(f.read())
    print(repr(USERID))
except FileNotFoundError:
    pass


command_update = 'dir > 1.txt'
command_build = 'dir > 2.txt'
command_get = 'dir > 3.txt'

proc_update = None
proc_build = None
proc_get = None


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    print(message.chat.id)
    await message.reply("Привет!\n /update - обновиться \n /build  - собрать проект \n /get - скачать файл")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler(commands=['build'])
async def build(message: types.Message):
    global proc_build
    global chat_id
    chat_id = message.chat.id
    
    if USERID !=  message.chat.id:
        return
    
    if not proc_build:
        proc_build = subprocess.Popen(
            (command_build),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
    
    print("build")
    
    
@dp.message_handler(commands=['update'])
async def update(message: types.Message):
    global proc_update
    global chat_id
    chat_id = message.chat.id
    
    if USERID !=  message.chat.id:
        return
    
    if not proc_update:
        proc_update = subprocess.Popen(
            (command_update),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
    
    print("update")


@dp.message_handler(commands=['get'])
async def get_file(message: types.Message):
    global proc_get
    global chat_id
    chat_id = message.chat.id
    
    if USERID !=  message.chat.id:
        return    
    
    if not proc_get:
        proc_get = subprocess.Popen(
            (command_get),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
    print("get file")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)
    

async def sender():
    global proc_update
    global proc_build
    global proc_get
    global chat_id
        
    while True:
        await asyncio.sleep(3)
        
 
        if proc_update:
            if proc_update.poll() is not None:
                proc_update = None
                await bot.send_message(chat_id, "update completed")
    
                
        if proc_build:
            if proc_build.poll() is not None:
                proc_build = None  
                await bot.send_message(chat_id, "build completed")
 
    
        if proc_get:
            if proc_get.poll() is not None:
                proc_get = None
                await bot.send_message(chat_id, "get completed")
                


if __name__ == '__main__':
    pass
    loop.create_task(sender())
    executor.start_polling(dp)