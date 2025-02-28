from typing import Final
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN : Final = "7766896429:AAHE9RR9XXXtvvgPVc9qlzZMMI53ihTt_VQ"
BOT_USERNAME : Final = "@AbitlyOpenDoorsBot"


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    [KeyboardButton("\U0001F50E Пошук"), KeyboardButton("\U0001F4CC Мої підписки")],
    [KeyboardButton("\U00002753 Довідка"), KeyboardButton("\U0001F4DD Зареєструватись")]
]
    
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text("Hello, this is a test version of OpenDoorsBot.", reply_markup= markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This bot just exist for helping microperson in their life")
    await update.message.reply_text(f"If u want something to know use  /info")


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Це також допоможе зрозуміти вам наш проєкт")
    await update.message.reply_text("Ви повинні знати: цей бот створений для пошуку інформації про День Відкритих Дверей")
    await update.message.reply_text("Це справді корисно для майбутніх студентів")



async def button_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text = update.message.text
  if text == "\U0001F4DD Зареєструватись":
      await update.message.reply_text("Ви обрали кнопку зареєструватись")
      await update.message.reply_text("Якщо ця опція вас влаштовує, то введіть ваше ім'я та прізвище")
    

async def button_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ви вибрали опцію мої підписки, бажаєте переглянути їх? Відповідайте 'так' або 'ні'.")
    context.user_data["waiting_for_confirmation"] = True 
       

async def button_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ви обрали кнопку пошуку")


async def button_dovidka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ви обрали кнопку довідка")


BUTTON_HANDLERS = {
    "\U0001F4CC мої підписки": button_sub,
    "\U0001F50E пошук": button_search,
    "\U00002753 довідка": button_dovidka,
    "\U0001F4DD зареєструватись": button_register
}
# Responses

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if context.user_data.get("waiting_for_confirmation"):
        if text == 'так':
            await update.message.reply_text("Ось ваші підписки:")
        else:
            await update.message.reply_text("Скасовано.")
        context.user_data["waiting_for_confirmation"] = False  
        return
    
        
    handler = BUTTON_HANDLERS.get(text)
    if handler:
        await handler(update, context)
    else:
        await update.message.reply_text("Я не розумію, що ви написали, будь ласка, оберіть коректний варіант.")


    

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.ALL, debug))
    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)


