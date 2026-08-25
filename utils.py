from datetime import date, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    """Create the main menu keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("🧮 Basic", callback_data='basic'),
            InlineKeyboardButton("📊 Percentage", callback_data='percentage'),
            InlineKeyboardButton("🏷️ Discount", callback_data='discount')
        ],
        [
            InlineKeyboardButton("💰 Compound", callback_data='compound'),
            InlineKeyboardButton("📏 Unit", callback_data='unit_convert'),
            InlineKeyboardButton("💾 Data-size", callback_data='data_size')
        ],
        [
            InlineKeyboardButton("⚖️ BMI", callback_data='bmi'),
            InlineKeyboardButton("🎂 Age", callback_data='age'),
            InlineKeyboardButton("📅 Date", callback_data='date')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def calculate_bmi(weight, height):
    """Calculate BMI."""
    return weight / (height ** 2)

def calculate_age(birth_date):
    """Calculate age from birth date."""
    today = date.today()
    
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day
    
    if days < 0:
        months -= 1
        # Get days in previous month
        prev_month = today.month - 1 or 12
        prev_year = today.year - 1 if prev_month == 12 else today.year
        days_in_prev_month = (date(prev_year, prev_month + 1, 1) - date(prev_year, prev_month, 1)).days
        days += days_in_prev_month
    
    if months < 0:
        years -= 1
        months += 12
    
    # Calculate days until next birthday
    next_birthday = date(today.year, birth_date.month, birth_date.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
    days_until_birthday = (next_birthday - today).days
    
    return {
        'years': years,
        'months': months,
        'days': days,
        'days_until_birthday': days_until_birthday
    }

def calculate_date_difference(date1, date2):
    """Calculate days between two dates."""
    return abs((date2 - date1).days)

def add_days_to_date(date, days):
    """Add days to a date."""
    return date + timedelta(days=days)

def subtract_days_from_date(date, days):
    """Subtract days from a date."""
    return date - timedelta(days=days)
