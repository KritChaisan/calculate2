def valid_text(value):
    return bool(value and value.strip())

def valid_positive_number(value):
    try:
        return float(value) >= 0
    except (ValueError, TypeError):
        return False

def valid_positive_int(value):
    try:
        return int(value) >= 0
    except (ValueError, TypeError):
        return False
