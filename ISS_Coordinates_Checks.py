import requests
from datetime import datetime
from Registrations import registrations
from Send_Email import send_email
import time


# Calls API to retrieve the ISS position (latitude and longiture)
def get_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    return iss_latitude, iss_longitude





# Empty dictionary of notified users. This will be used to check if the user has already been notified when
# their coordinates are within range of the ISS' position, so as to ensure only one notification (ie. email)
# is sent to the user at a time

notified_users = {}


#Every 10 seconds, it checks whether any one user's coordinates are within 5 degrees each way of the ISS' position.

# Once the user has been notified of their proximity to the ISS' coordinates, they will no longer be nofitied until the
# next time their and the ISS coordinates align

def check_iss_and_notify():
    while True:
        iss_latitude, iss_longitude = get_iss_position()
        for email_address, coords in registrations.items():
            latitude, longitude = coords
            lat = float(latitude)
            lon = float(longitude)
            if (abs(iss_latitude - lat) <= 5.0 and abs(iss_longitude - lon) <= 5.0):
                if email_address not in notified_users:
                    if send_email(email_address):
                        notified_users[email_address] = True
            elif email_address in notified_users:
                del notified_users[email_address]

        time.sleep(10)
