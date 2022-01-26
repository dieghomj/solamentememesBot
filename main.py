import logging
import os
import time

from telegram import Update
from telegram.ext import Updater, CommandHandler, Filters, CallbackContext
from telegram.ext.messagehandler import MessageHandler
from telegram.files.file import File

from twitter import upload_photo, upload_video

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        update.message.reply_text(
            '''Bot del canal @Solamentememes'''
        )


def ask_Channel(update: Update, context: CallbackContext) -> bool:
    chat_name = update.channel_post.chat.username
    # chat_type = update.channel_post.chat.type

    if chat_name.casefold() in ['solamentememes', 'testchannelsolamentememes']:
        return True
    else:
        return False


meme_uploaded = False


def erase():
    global meme_uploaded

    if meme_uploaded:
        meme_uploaded = False
        if os.path.exists('photo.jpg'):
            os.remove('photo.jpg')
        else:
            if os.path.exists('video.mp4'):
                os.remove('video.mp4')
            else:
                print('ERROR: any of this files exists!')
    else:
        print('Meme not uploaded, but downloaded next meme will overwrite this one')


def get_memes_photo(update: Update, context: CallbackContext) -> None:
    global meme_uploaded

    if ask_Channel(update, context):
        photo = update.channel_post.photo[2].get_file()

        file_dir = 'photo.jpg'
        File.download(photo, file_dir)

        meme_uploaded = upload_photo()
        time.sleep(100)
        erase()


def get_memes_video(update: Update, context: CallbackContext) -> None:
    global meme_uploaded

    if ask_Channel(update, context):
        video = update.channel_post.video.get_file()

        file_dir = 'video.mp4'
        File.download(video, file_dir)

        meme_uploaded = upload_video()
        time.sleep(100)
        erase()


if __name__ == '__main__':
    updater = Updater('TELEGRAM_API_KEY', use_context=True)
    dp = updater.dispatcher
    # Handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.photo & (~Filters.command), get_memes_photo))
    dp.add_handler(MessageHandler(Filters.video & (~Filters.command), get_memes_video))

    updater.start_polling()
    updater.idle()
