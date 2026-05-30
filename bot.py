import os
import sqlite3
import random
import telebot

# Token Render platformasida o'zgaruvchi sifatida kiritiladi
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlar bazasini guruh xabarlari uchun sozlash
conn = sqlite3.connect("chat_memory.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT UNIQUE)''')
conn.commit()

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # Faqat guruh va superguruhlarda ishlashi uchun
    if message.chat.type in ['group', 'supergroup']:
        text = message.text
        # Agar matn bo'lsa va buyruq (/) bo'lmasa bazaga yozadi
        if text and not text.startswith('/'):
            try:
                cursor.execute("INSERT OR IGNORE INTO messages (text) VALUES (?)", (text,))
                conn.commit()
            except:
                pass
            
            # Har 3 ta xabardan biriga tasodifiy javob qaytarish ehtimoli
            if random.randint(1, 3) == 1:
                cursor.execute("SELECT text FROM messages ORDER BY RANDOM() LIMIT 1")
                row = cursor.fetchone()
                if row:
                    bot.reply_to(message, row[0])

if __name__ == "__main__":
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()
  
