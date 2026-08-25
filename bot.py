import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import handlers
from utils import get_main_menu_keyboard

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    welcome_message = f"""👋 Hello {user.first_name}!

Welcome to @sonlyculatorbot - Your All-in-One Calculator Bot!

I can help you with:
🧮 Basic Calculations
📊 Percentages
🏷️ Discounts
💰 Compound Interest
📏 Unit Conversions
💾 Data-size Conversions
⚖️ BMI Calculator
🎂 Age Calculator
📅 Date Calculator

Use the buttons below to get started or type /help for more info!"""

    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_menu_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when /help is issued."""
    help_text = """
🤖 *Sonlyculator Bot Help*

Here's how to use each feature:

🔢 *Basic Calculations*
Type any mathematical expression like: 2+2, 10*5, (3+2)*4

📊 *Percentages*
Type: percentage X% of Y (e.g., percentage 20% of 100)

🏷️ *Discounts*
Type: discount original_price discount_percentage (e.g., discount 100 20)

💰 *Compound Interest*
Type: compound principal rate time (e.g., compound 1000 5 2)

📏 *Unit Conversions*
• Length: length 5 km to m
• Weight: weight 10 kg to g
• Temperature: temp 100 c to f

💾 *Data-size*
Type: data 1024 MB to GB

⚖️ *BMI Calculator*
Type: bmi weight height (e.g., bmi 70 1.75)

🎂 *Age Calculator*
Type: age YYYY-MM-DD (e.g., age 1990-01-15)

📅 *Date Calculator*
• Add days: date add YYYY-MM-DD days
• Subtract days: date sub YYYY-MM-DD days
• Days between: date between YYYY-MM-DD YYYY-MM-DD

Use the menu buttons below to access features easily!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    action = query.data
    context.user_data['last_action'] = action
    
    messages = {
        'basic': "🔢 *Basic Calculator*\n\nSend me any mathematical expression like:\n`2+2`, `10*5`, `(3+2)*4`, `sqrt(16)`, `sin(30)`\n\nSupported: +, -, *, /, ^, sqrt, sin, cos, tan, log, ln",
        'percentage': "📊 *Percentage Calculator*\n\nSend me: `percentage X% of Y`\nExample: `percentage 20% of 100`",
        'discount': "🏷️ *Discount Calculator*\n\nSend me: `discount original_price discount_percentage`\nExample: `discount 100 20`",
        'compound': "💰 *Compound Interest Calculator*\n\nSend me: `compound principal rate time`\nExample: `compound 1000 5 2`\n(rate in %, time in years)",
        'unit_convert': "📏 *Unit Conversion*\n\nAvailable conversions:\n• Length: `length 5 km to m`\n• Weight: `weight 10 kg to g`\n• Temperature: `temp 100 c to f`",
        'data_size': "💾 *Data-size Conversion*\n\nSend me: `data value unit to unit`\nExample: `data 1024 MB to GB`\nUnits: B, KB, MB, GB, TB",
        'bmi': "⚖️ *BMI Calculator*\n\nSend me: `bmi weight height`\nExample: `bmi 70 1.75`\n(weight in kg, height in meters)",
        'age': "🎂 *Age Calculator*\n\nSend me: `age YYYY-MM-DD`\nExample: `age 1990-01-15`",
        'date': "📅 *Date Calculator*\n\n• Add days: `date add YYYY-MM-DD days`\n• Subtract days: `date sub YYYY-MM-DD days`\n• Days between: `date between YYYY-MM-DD YYYY-MM-DD`"
    }
    
    await query.edit_message_text(
        messages.get(action, "Feature coming soon!"),
        parse_mode='Markdown',
        reply_markup=get_main_menu_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    text = update.message.text
    response = handlers.process_message(text, context)
    await update.message.reply_text(response, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Start the bot."""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
