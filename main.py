import os
from typing import Final
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN: Final = os.environ.get('BOT_TOKEN')
BOT_USERNAME : Final = "@AbitlyOpenDoorsBot"


USER_DATA = {}
FIRST_NAME = range(1)


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    [KeyboardButton("\U0001F50E Пошук"), KeyboardButton("\U0001F4CC Мої підписки")],
    [KeyboardButton("\U0001F4DA Довідка"), KeyboardButton("\U0001F4DD Зареєструватись")]
]
    
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text("Вас вітає OpenDoorsBot, це поки що тестова версія!", reply_markup= markup)
    await update.message.reply_text("Щоб дізнатися покрокову інформацію натисність кнопку \n \U0001F4DA Довідка")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Цей бот був створений для облегшення життя абітурієнтам.")
    await update.message.reply_text("А саме облегшена версія пошуку інформації про день відкритих дверей")
    await update.message.reply_text("Якщо ви хочете дізнатися більше натисність /info")


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тут ви більше зможете дізнатися про наш проєкт.")
    await update.message.reply_text("В боті ви зможете відслідовувати інформацію про день відкритих дверей в бажаному ЗВО!")
    await update.message.reply_text("Це насправді дуже корисно для вас, і зараз я розповім, як вам почати це робити!")
    await update.message.reply_text("Натиcніть кнопку \U0001F50E Пошук, оберіть заклад, який вам цікавий")
    await update.message.reply_text("Якщо інформація вже відома про захід, ми вам скажемо, якщо ні, то у майбутньому обо'язково вас повідомимо!")



async def button_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ви обрали кнопку зареєструватись")
    await update.message.reply_text("Якщо ця опція вас влаштовує, то введіть ваше ім'я")
    context.user_data["waiting_for_reg"] = True 


async def button_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ви вибрали опцію мої підписки, бажаєте переглянути їх? Відповідайте 'так' або 'ні'.")
    context.user_data["waiting_for_sub"] = True 
       

async def button_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ви обрали кнопку пошуку")
    context.user_data["waiting_for_search"] = True 

async def button_ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ви обрали кнопку \U0001F4DA  Довідка")
    await help_command(update, context)
    context.user_data["waiting_for_ref"] = True 


BUTTON_HANDLERS = {
    "\U0001F4CC мої підписки": button_sub,
    "\U0001F50E пошук": button_search,
    "\U0001F4DA довідка": button_ref,
    "\U0001F4DD зареєструватись": button_register
}

# Responses

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    print(f"Recieved: {text}")
    print(update)

    if context.user_data.get("waiting_for_sub"):
        if text == 'так':
            await update.message.reply_text("Ось ваші підписки:")
        else:
            await update.message.reply_text("Скасовано.")
        context.user_data["waiting_for_sub"] = False  
        return
    
    if context.user_data.get("waiting_for_reg"):
        user_id = update.message.from_user.id
        USER_DATA[user_id] = {"first_name": text}  
        await update.message.reply_text(f"Ваше ім'я збережено: {text.capitalize()}")
        await update.message.reply_text("Ви успішно зареєструвались \U00002705")
        context.user_data["waiting_for_reg"] = False 
        return
    
            
    handler = BUTTON_HANDLERS.get(text)
    if handler:
        await handler(update, context)
    else:
        await update.message.reply_text("Я не розумію, що ви написали, будь ласка, оберіть коректний варіант.")
    

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Реєстрацію скасовано.")
    context.user_data["waiting_for_reg"] = False
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('info', info_command))

    # Messages
    app.add_handler(MessageHandler(filters.Regex("^\U0001F4DA  Довідка$"), button_ref))
    app.add_handler(MessageHandler(filters.Regex("^\U0001F4DD  Зареєструватись$"), button_register))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.ALL, debug))
    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)


