import re
import math
from datetime import datetime, timedelta
from utils import calculate_bmi, calculate_age, calculate_date_difference, add_days_to_date, subtract_days_from_date

def process_message(text, context):
    """Process user messages and route to appropriate handler."""
    text = text.strip().lower()
    
    # Check for different command types
    if text.startswith('percentage'):
        return handle_percentage(text)
    elif text.startswith('discount'):
        return handle_discount(text)
    elif text.startswith('compound'):
        return handle_compound_interest(text)
    elif text.startswith('length'):
        return handle_length_conversion(text)
    elif text.startswith('weight'):
        return handle_weight_conversion(text)
    elif text.startswith('temp'):
        return handle_temperature_conversion(text)
    elif text.startswith('data'):
        return handle_data_conversion(text)
    elif text.startswith('bmi'):
        return handle_bmi(text)
    elif text.startswith('age'):
        return handle_age(text)
    elif text.startswith('date'):
        return handle_date_calculator(text)
    else:
        # Try basic calculation
        return handle_basic_calculation(text)

def handle_basic_calculation(text):
    """Handle basic mathematical calculations."""
    # Remove any dangerous characters
    text = re.sub(r'[^0-9+\-*/().%^ ]', '', text)
    
    # Replace ^ with ** for exponentiation
    text = text.replace('^', '**')
    
    # Add mathematical functions
    allowed_names = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'log': math.log10,
        'ln': math.log,
        'pi': math.pi,
        'e': math.e
    }
    
    try:
        # Safe evaluation
        result = eval(text, {"__builtins__": {}}, allowed_names)
        return f"✅ Result: {result:.10f}".rstrip('0').rstrip('.')
    except:
        return "❌ Invalid expression. Please check your input."

def handle_percentage(text):
    """Calculate percentage."""
    try:
        # Parse: percentage X% of Y
        match = re.search(r'percentage\s+([\d.]+)%?\s+of\s+([\d.]+)', text)
        if not match:
            return "❌ Please use format: `percentage X% of Y`"
        
        percentage = float(match.group(1))
        value = float(match.group(2))
        result = (percentage / 100) * value
        return f"✅ {percentage}% of {value} = {result:.2f}"
    except:
        return "❌ Invalid input. Please use: `percentage 20% of 100`"

def handle_discount(text):
    """Calculate discount."""
    try:
        # Parse: discount original_price discount_percentage
        match = re.search(r'discount\s+([\d.]+)\s+([\d.]+)', text)
        if not match:
            return "❌ Please use format: `discount original_price discount_percentage`"
        
        original = float(match.group(1))
        discount_percent = float(match.group(2))
        
        discount_amount = (discount_percent / 100) * original
        final_price = original - discount_amount
        
        return f"""✅ Discount Calculation:
💰 Original Price: ${original:.2f}
🏷️ Discount: {discount_percent}%
💲 Discount Amount: ${discount_amount:.2f}
💵 Final Price: ${final_price:.2f}"""
    except:
        return "❌ Invalid input. Please use: `discount 100 20`"

def handle_compound_interest(text):
    """Calculate compound interest."""
    try:
        # Parse: compound principal rate time
        match = re.search(r'compound\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', text)
        if not match:
            return "❌ Please use format: `compound principal rate time`"
        
        principal = float(match.group(1))
        rate = float(match.group(2)) / 100
        time = float(match.group(3))
        
        amount = principal * (1 + rate) ** time
        interest = amount - principal
        
        return f"""✅ Compound Interest:
💰 Principal: ${principal:.2f}
📊 Rate: {match.group(2)}%
⏰ Time: {time} years
💵 Total Amount: ${amount:.2f}
📈 Interest Earned: ${interest:.2f}"""
    except:
        return "❌ Invalid input. Please use: `compound 1000 5 2`"

def handle_length_conversion(text):
    """Convert length units."""
    conversions = {
        'km': 1000,
        'm': 1,
        'cm': 0.01,
        'mm': 0.001,
        'mile': 1609.34,
        'yard': 0.9144,
        'foot': 0.3048,
        'inch': 0.0254
    }
    
    try:
        match = re.search(r'length\s+([\d.]+)\s+(\w+)\s+to\s+(\w+)', text)
        if not match:
            return "❌ Please use format: `length value unit to unit`"
        
        value = float(match.group(1))
        from_unit = match.group(2).lower()
        to_unit = match.group(3).lower()
        
        if from_unit not in conversions or to_unit not in conversions:
            return "❌ Invalid units. Supported: km, m, cm, mm, mile, yard, foot, inch"
        
        # Convert to meters first, then to target unit
        meters = value * conversions[from_unit]
        result = meters / conversions[to_unit]
        
        return f"✅ {value} {from_unit} = {result:.4f} {to_unit}"
    except:
        return "❌ Invalid input. Please use: `length 5 km to m`"

def handle_weight_conversion(text):
    """Convert weight units."""
    conversions = {
        'kg': 1,
        'g': 0.001,
        'mg': 0.000001,
        'lb': 0.453592,
        'oz': 0.0283495
    }
    
    try:
        match = re.search(r'weight\s+([\d.]+)\s+(\w+)\s+to\s+(\w+)', text)
        if not match:
            return "❌ Please use format: `weight value unit to unit`"
        
        value = float(match.group(1))
        from_unit = match.group(2).lower()
        to_unit = match.group(3).lower()
        
        if from_unit not in conversions or to_unit not in conversions:
            return "❌ Invalid units. Supported: kg, g, mg, lb, oz"
        
        kg = value * conversions[from_unit]
        result = kg / conversions[to_unit]
        
        return f"✅ {value} {from_unit} = {result:.4f} {to_unit}"
    except:
        return "❌ Invalid input. Please use: `weight 10 kg to g`"

def handle_temperature_conversion(text):
    """Convert temperature."""
    try:
        match = re.search(r'temp\s+([\d.]+)\s+(\w+)\s+to\s+(\w+)', text)
        if not match:
            return "❌ Please use format: `temp value unit to unit`"
        
        value = float(match.group(1))
        from_unit = match.group(2).lower()
        to_unit = match.group(3).lower()
        
        # Convert to Celsius first
        if from_unit == 'c':
            celsius = value
        elif from_unit == 'f':
            celsius = (value - 32) * 5/9
        elif from_unit == 'k':
            celsius = value - 273.15
        else:
            return "❌ Invalid units. Supported: C, F, K"
        
        # Convert from Celsius to target
        if to_unit == 'c':
            result = celsius
        elif to_unit == 'f':
            result = celsius * 9/5 + 32
        elif to_unit == 'k':
            result = celsius + 273.15
        else:
            return "❌ Invalid units. Supported: C, F, K"
        
        return f"✅ {value}°{from_unit.upper()} = {result:.2f}°{to_unit.upper()}"
    except:
        return "❌ Invalid input. Please use: `temp 100 c to f`"

def handle_data_conversion(text):
    """Convert data sizes."""
    units = ['b', 'kb', 'mb', 'gb', 'tb']
    multipliers = {
        'b': 1,
        'kb': 1024,
        'mb': 1024**2,
        'gb': 1024**3,
        'tb': 1024**4
    }
    
    try:
        match = re.search(r'data\s+([\d.]+)\s+(\w+)\s+to\s+(\w+)', text)
        if not match:
            return "❌ Please use format: `data value unit to unit`"
        
        value = float(match.group(1))
        from_unit = match.group(2).lower()
        to_unit = match.group(3).lower()
        
        if from_unit not in multipliers or to_unit not in multipliers:
            return "❌ Invalid units. Supported: B, KB, MB, GB, TB"
        
        bytes_value = value * multipliers[from_unit]
        result = bytes_value / multipliers[to_unit]
        
        return f"✅ {value} {from_unit.upper()} = {result:.4f} {to_unit.upper()}"
    except:
        return "❌ Invalid input. Please use: `data 1024 MB to GB`"

def handle_bmi(text):
    """Calculate BMI."""
    try:
        match = re.search(r'bmi\s+([\d.]+)\s+([\d.]+)', text)
        if not match:
            return "❌ Please use format: `bmi weight height`"
        
        weight = float(match.group(1))
        height = float(match.group(2))
        
        result = calculate_bmi(weight, height)
        
        # Determine BMI category
        if result < 18.5:
            category = "Underweight"
        elif result < 25:
            category = "Normal weight"
        elif result < 30:
            category = "Overweight"
        else:
            category = "Obese"
        
        return f"""✅ BMI Calculation:
⚖️ Weight: {weight} kg
📏 Height: {height} m
📊 BMI: {result:.1f}
📋 Category: {category}"""
    except:
        return "❌ Invalid input. Please use: `bmi 70 1.75`"

def handle_age(text):
    """Calculate age."""
    try:
        match = re.search(r'age\s+(\d{4}-\d{2}-\d{2})', text)
        if not match:
            return "❌ Please use format: `age YYYY-MM-DD`"
        
        birth_date = datetime.strptime(match.group(1), '%Y-%m-%d').date()
        age_info = calculate_age(birth_date)
        
        return f"""✅ Age Calculator:
📅 Birth Date: {birth_date}
🎂 Age: {age_info['years']} years, {age_info['months']} months, {age_info['days']} days
⏳ Days until next birthday: {age_info['days_until_birthday']} days
"""
    except:
        return "❌ Invalid date. Please use: `age 1990-01-15`"

def handle_date_calculator(text):
    """Handle date calculations."""
    try:
        if text.startswith('date add'):
            match = re.search(r'date add\s+(\d{4}-\d{2}-\d{2})\s+(\d+)', text)
            if match:
                date = datetime.strptime(match.group(1), '%Y-%m-%d').date()
                days = int(match.group(2))
                result = add_days_to_date(date, days)
                return f"✅ {date} + {days} days = {result}"
        
        elif text.startswith('date sub'):
            match = re.search(r'date sub\s+(\d{4}-\d{2}-\d{2})\s+(\d+)', text)
            if match:
                date = datetime.strptime(match.group(1), '%Y-%m-%d').date()
                days = int(match.group(2))
                result = subtract_days_from_date(date, days)
                return f"✅ {date} - {days} days = {result}"
        
        elif text.startswith('date between'):
            match = re.search(r'date between\s+(\d{4}-\d{2}-\d{2})\s+(\d{4}-\d{2}-\d{2})', text)
            if match:
                date1 = datetime.strptime(match.group(1), '%Y-%m-%d').date()
                date2 = datetime.strptime(match.group(2), '%Y-%m-%d').date()
                days = calculate_date_difference(date1, date2)
                return f"✅ Days between {date1} and {date2}: {days} days"
        
        return "❌ Invalid format. Use:\n• `date add YYYY-MM-DD days`\n• `date sub YYYY-MM-DD days`\n• `date between YYYY-MM-DD YYYY-MM-DD`"
    except:
        return "❌ Invalid input. Please check your date format."
