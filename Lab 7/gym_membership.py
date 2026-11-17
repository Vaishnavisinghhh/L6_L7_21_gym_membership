import math


def parse_plan(code):
    """Parse a plan code like 'GOLD-12' -> ('GOLD', 12).
    Returns None for any invalid input instead of crashing."""
    if not isinstance(code, str):
        return None
    parts = code.strip().split('-')
    if len(parts) != 2:
        return None
    plan, months = parts[0].strip(), parts[1].strip()
    if not plan or not plan.isalpha():
        return None
    if not months.isascii() or not months.isdigit():
        return None
    try:
        months = int(months)
    except ValueError:  # e.g. absurdly long digit strings
        return None
    if months <= 0:
        return None
    return plan.upper(), months


def calculate_bmi(data):
    """Parse 'weight,height' and return BMI rounded to 1 dp.
    Returns None for any invalid input instead of crashing."""
    if not isinstance(data, str):
        return None
    parts = data.split(',')
    if len(parts) != 2:
        return None
    try:
        weight = float(parts[0])
        height = float(parts[1])
        if not (math.isfinite(weight) and math.isfinite(height)):
            return None
        if weight <= 0 or height <= 0:
            return None
        bmi = weight / (height ** 2)
    except (ValueError, OverflowError, ZeroDivisionError):
        return None
    if not math.isfinite(bmi):
        return None
    return round(bmi, 1)


def average_workout(minutes):
    """Average of space-separated workout minutes (integer division).
    Returns None for any invalid input instead of crashing."""
    if not isinstance(minutes, str):
        return None
    tokens = minutes.split()
    if not tokens:
        return None
    values = []
    for t in tokens:
        if not t.isascii() or not t.isdigit():
            return None
        try:
            values.append(int(t))
        except ValueError:
            return None
    return sum(values) // len(values)


def main():
    print("==== Running parse_plan ====")
    try:
        user_input = input("Enter a plan code (e.g. GOLD-12): ")
    except EOFError:
        user_input = ""
    result = parse_plan(user_input)
    if result is None:
        print("Invalid plan code. Expected format: NAME-MONTHS (e.g. GOLD-12)")
    else:
        print("Plan and Months:", result)

    print("\n==== Running calculate_bmi ====")
    try:
        user_input = input("Enter weight and height (e.g. 70,1.75): ")
    except EOFError:
        user_input = ""
    result = calculate_bmi(user_input)
    if result is None:
        print("Invalid input. Expected: weight,height (positive numbers)")
    else:
        print("BMI:", result)

    print("\n==== Running average_workout ====")
    try:
        user_input = input("Enter workout minutes separated by spaces (e.g. 45 60 30): ")
    except EOFError:
        user_input = ""
    result = average_workout(user_input)
    if result is None:
        print("Invalid input. Expected: whole numbers separated by spaces")
    else:
        print("Average Minutes:", result)


if __name__ == "__main__":
    main()
