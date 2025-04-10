from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import instaloader
import os
import shutil

# Instaloader instansiyasi
L = instaloader.Instaloader()

# Botni yaratish
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Salom! Instagram video havolasini yuboring.')

# Instagram video yuklash funksiyasi
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Foydalanuvchidan URL olish
    url = update.message.text
    try:
        # Instagram postni yuklash
        post = instaloader.Post.from_shortcode(L.context, url.split('/')[-2])

        # Video yuklash
        target_directory = f"{post.owner_username}_post"
        L.download_post(post, target=target_directory)

        # Video faylni topish
        video_file = None
        for filename in os.listdir(target_directory):
            if filename.endswith(".mp4"):
                video_file = os.path.join(target_directory, filename)
                break

        if video_file:
            # Video faylini Telegramga yuborish
            with open(video_file, 'rb') as video:
                await update.message.reply_video(video)

            # Yuklangan faylni o'chirish (ixtiyoriy)
            os.remove(video_file)

            # Katalogni tozalash va o'chirish
            shutil.rmtree(target_directory)

            # Foydalanuvchiga video yuklandi deb habar yuborish
            await update.message.reply_text('Botimizdan foydalanganingiz uchun rahmat ❤️')
        else:
            await update.message.reply_text("Video fayli topilmadi.")

    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")

# Botni sozlash
def main():
    # API Tokenni o'zgartiring
    API_TOKEN = '7223895971:AAFW6eK71QjeQYWqtGQYPK0XDfsr9xGF9vA'
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT, download_video))  # Barcha matnli xabarlarni tekshiradi

    application.run_polling()

if __name__ == "__main__":
    main()

