from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os
import time

import subprocess

import asyncio

loop = asyncio.get_event_loop()

chat_id = -1

TOKEN = ""

USERID = ""

workdir = r"H:\arduino_work_proj\MyHouse_kivy_app"

filename_apk = r"\bin\myhouse-0.1-arm64-v8a_armeabi-v7a-debug.apk"

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


command_update = 'git pull'

command_build = r'docker run --rm --cpus 10 -v %cd%:/home/user/buildozer/ -v C:\buildozer:/home/user/.buildozer/ queirozt/kivy-buildozer buildozer android debug'

command_get = 'dir > 3.txt'

proc_update = None
proc_build = None
proc_get = None

old_filetime = 0
build_start_time = 0

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def get_filetime():
    return time.time() - os.path.getmtime(workdir + filename_apk)

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
        global old_filetime 
        global build_start_time
        old_filetime = get_filetime()
        build_start_time = time.time()

        proc_build = subprocess.Popen(
            (command_build),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=workdir
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
            cwd=workdir
        )
    
    print("update")


@dp.message_handler(commands=['get'])
async def get_file(message: types.Message):
    global proc_get
    global chat_id
    chat_id = message.chat.id
    
    if USERID !=  message.chat.id:
        return    
    
    # if not proc_get:
    #     proc_get = subprocess.Popen(
    #         (command_get),
    #         stdin=subprocess.PIPE,
    #         stdout=subprocess.PIPE,
    #         shell=True,
    #         cwd=workdir
    #     )
    
    with open(os.path.join(workdir, filename_apk), 'rb') as file:
         await bot.send_document(chat_id, file, disable_notification=True)


    # if platform.system() == 'Windows':
    print(get_filetime())

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
 
    
        # if proc_get:
        #     if proc_get.poll() is not None:
        #         proc_get = None
        #         await bot.send_message(chat_id, "get completed")


        global old_filetime 
        filetime = get_filetime()
        if filetime < old_filetime:
            if filetime > 10:
                await bot.send_message(chat_id, "file created!\nTime: " + str(int(time.time() - build_start_time)) + " seconds")
                proc_build.kill()
                old_filetime = filetime 



if __name__ == '__main__':
    pass
    loop.create_task(sender())
    executor.start_polling(dp)