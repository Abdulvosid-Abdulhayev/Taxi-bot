import telebot

# Telegram bot tokenini kiriting
API_TOKEN = "Token"

# Guruh IDlarini kiriting
GROUP_1_ID = -1234567890123  # Group ID
GROUP_2_ID = -1234567890123

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Farg'ona - Toshkent taxi\n Toshkent - Farg'ona \n Bot ishga tushdi")

# Bu funksiya birinchi guruhdan kelgan habarlarni ikkinchi guruhga yuboradi, agar foydalanuvchi ikkinchi guruhda bo'lmasa
@bot.message_handler(func=lambda message: message.chat.id == GROUP_1_ID)
def move_to_group_2(message):
    try:
        # Foydalanuvchi maqomini tekshirish
        user_status = bot.get_chat_member(GROUP_2_ID, message.from_user.id).status
        print(f"User status in group 2: {user_status}")  # Debugging maqsadida 
        if user_status not in ['member', 'administrator', 'creator']:
            # Foydalanuvchining to'liq ismini olish
            full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()

            # Foydalanuvchi username ni olish
            username = message.from_user.username
            if username:
                user_link = f'<a href="https://t.me/{username}">{full_name}</a>'
            else:
                user_link = f'<a href="tg://user?id={message.from_user.id}">{full_name}</a>'
            
            # Xabarni yangi formatda ikkinchi guruhga yuborish
            formatted_message = (
                f"{user_link} (profil):\n"
                f"✉️ Xabar: {message.text}\n"
                f"👤 Ism: {message.from_user.first_name}\n"
                f"📶 Username: @{username if username else 'username mavjud emas'}\n"
                f"📬 Profil: {user_link}\n\n"
                "💬 Guruh: FARGʻONA TOSHKENT TAXI"
            )
            bot.send_message(GROUP_2_ID, formatted_message, parse_mode='HTML', disable_web_page_preview=True)
            
            # Xabarni birinchi guruhdan o'chirish
            bot.delete_message(GROUP_1_ID, message.message_id)
            print(f"Xabar ko'chirildi va o'chirildi: {message.text}")
            
            # Foydalanuvchiga xabar yuborish
            reply_message = (
                f"Assalomu alaykum {full_name},\n"
                "☎️ Sizga shofyorlar aloqaga chiqadi!\n"
                "✅ Lichkada ishonchli haydovchi sizni kutmoqda!\n"
                "🔗 Guruh sizga maqul bo'lsa iltimos do'stlaringizga ham ulashing. Rahmat😊❗️"
            )
            bot.send_message(message.chat.id, reply_message)
        else:
            print("Foydalanuvchi ikkinchi guruh a'zosi. Xabar ko'chirilmadi.")
    except telebot.apihelper.ApiException as e:
        print(f"Xabarni qayta ishlashda xatolik: {e}")

# Botni ishga tushiramiz
bot.infinity_polling()
