import uuid

def generate_7_digit_uuid():
    # Generate a UUID
    full_uuid = uuid.uuid4().int  # Get the UUID as a 128-bit integer

    # Truncate to 7 digits
    short_uuid = full_uuid % 10_000_000  # Modulo operation to get the last 7 digits

    # Pad with leading zeros to ensure 7 digits
    return f"{short_uuid:07}"  # Format as a 7-digit string with leading zeros