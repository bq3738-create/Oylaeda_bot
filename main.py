import os
import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ALLOWED_USERS = [int(x) for x in os.environ.get("ALLOWED_USERS", "").split(",") if x.strip()]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.id not in ALLOWED_USERS:
        bot.reply_to(message, "Kechirasiz, sizga bu botdan foydalanishga ruxsat berilmagan.")
        return
    bot.reply_to(message, "Assalomu alaykum! Taom rasmini yuboring, men uning kaloriyasi va tarkibini hisoblab beraman!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.from_user.id not in ALLOWED_USERS:
        return

    bot.reply_to(message, "Rasm tahlil qilinmoqda, biroz kuting...")

    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        image_data = {
            "mime_type": "image/jpeg",
            "data": downloaded_file
        }

        prompt = (
            "Rasmdagi taomni aniqla. Nomi, taxminiy vazni (grammda), "
            "kaloriyasi (kkal), oqsillar, yog'lar va uglevodlar miqdorini ko'rsat. "
            "Javobni o'zbek tilida, qisqa va tushunarli yoz."
        )

        response = model.generate_content([prompt, image_data])
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")

bot.infinity_polling()
