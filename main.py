import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
)

import constants
from utils import extract_lat_long_via_address, get_weather

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

BOT_TOKEN = constants.BOT_TOKEN
LOCATION_INPUT = 1
CONFIRMATION = 2


async def start(update: Update, context: CallbackContext):
    context.user_data["location"] = None
    await update.message.reply_text("Please enter your location or type /cancel to cancel:")

    return LOCATION_INPUT


async def get_location(update: Update, context: CallbackContext):
    entered_location = update.message.text

    latitude, longitude, location = extract_lat_long_via_address(entered_location)  # Replace with actual coordinates
    coordinates = {"lat": latitude, "lng": longitude}
    if location is None:
        await update.message.reply_text("Sorry, I couldn't find that location. Please try again:")
        return LOCATION_INPUT
    if latitude is not None and longitude is not None:
        weather = await get_weather(update, context, coordinates)
        await update.message.reply_text(f"The weather in {location} is {weather['temperature']}°C right now.")
        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data="yes"),
                InlineKeyboardButton("No", callback_data="no"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Is this your location?", reply_markup=reply_markup)
        return CONFIRMATION


async def confirmation(update: Update, context: CallbackContext):
    query = update.callback_query
    user_response = query.data

    if user_response == "yes":
        await query.message.reply_text("Great! Bye!", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    elif user_response == "no":
        await query.message.reply_text("Please enter your location again or type /cancel to cancel:")
        return LOCATION_INPUT


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Location input canceled.", reply_markup=ReplyKeyboardRemove())
    # Reset the conversation state
    return ConversationHandler.END


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LOCATION_INPUT: [MessageHandler(None, get_location)],
            CONFIRMATION: [CallbackQueryHandler(confirmation, pattern="^(yes|no)$")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conversation_handler)

    application.run_polling()
