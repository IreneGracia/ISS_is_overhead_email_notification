
# Validating that the latitude and longitude keyboard inputs are valid
def validate_coordinates(latitude, longitude):
    if not latitude or not longitude:
        raise ValueError("Both latitude and longitude must be provided. Please enter valid coordinates.")
    try:
        lat, lon = float(latitude), float(longitude)
    except ValueError:
        raise ValueError("Coordinates must be numeric. Please enter valid numeric values for latitude and longitude.")

    if not (-90 <= lat <= 90):
        raise ValueError(f"Latitude must be between -90.0 and 90.0 degrees. Got {lat} instead. Please go back and submit valid coordinates.")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Longitude must be between -180.0 and 180.0 degrees. Got: {lon} instead. Please go back and submit valid coordinates.")

    return lat, lon



# Validates that the email address text box was not left empty (even accounting for blank spaces)
def validate_email(email_address):
    if not email_address or not email_address.strip():
        raise ValueError('A valid email address must be provided.')
    return email_address
