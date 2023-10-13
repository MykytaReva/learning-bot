import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, ContextTypes, MessageHandler, filters

import constants
from utils import extract_lat_long_via_address, get_weather

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

BOT_TOKEN = constants.BOT_TOKEN


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am Weather/Location bot, please type something so I can respond!")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Custom commands are not implemented yet, sorry!")


# responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "Hello there!"
    if "bye" in processed:
        return "Goodbye!"
    if "weather" in processed:
        return "The weather is nice!"
    return "Sorry, I don't understand you!"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    logging.info(f"User {update.message.chat.id} in {message_type}: {text}")
    if message_type == "group" or message_type == "supergroup":
        if constants.BOT_USERNAME in text:
            new_text = text.replace(constants.BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return None
    else:
        response = handle_response(text)
    await update.message.reply_text(response)


async def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logging.warning(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("custom", custom_command))

    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_error_handler(error)

    application.run_polling(pool_timeout=3)
