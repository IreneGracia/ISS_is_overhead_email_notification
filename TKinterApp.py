import tkinter as tk
from Registrations import registrations
from ISS_Coordinates_Checks import check_iss_and_notify
import threading
from Validations import validate_coordinates, validate_email


WIDTH = 500
HEIGHT = 700

window = tk.Tk()
window.title('ISS Notifier')
window.minsize(width=WIDTH, height=HEIGHT)

# Global variables for widgets
label_intro = None
label_email = None
textbox_email = None
label_coordinates = None
label_longitude = None
textbox_longitude = None
label_latitude = None
textbox_latitude = None
button = None



def setup_main_ui():

    # Ensuring we are working with global variables, and that no new variables are created by this function
    global label_intro, label_email, textbox_email, label_coordinates, label_longitude, textbox_longitude, label_latitude, textbox_latitude, button

    # Clear existing widgets
    for widget in window.winfo_children():
        widget.destroy()

    # Intro widgets
    label_intro = tk.Label(window, text='Welcome to the ISS notifier.', font=('Arial', 24, 'bold'))
    label_intro.place(x=WIDTH/2, y=100, anchor='center')

    # Email widgets
    label_email = tk.Label(window, text='Insert your email address below:', font=('Arial', 24, 'bold'))
    label_email.place(x=WIDTH/2, y=200, anchor='center')

    textbox_email = tk.Entry(width=50)
    textbox_email.place(x=WIDTH/2, y=250, anchor='center')

    # Coordinate entry widgets
    label_coordinates = tk.Label(window, text='Now insert your coordinates:', font=('Arial', 24, 'bold'))
    label_coordinates.place(x=WIDTH/2, y=340, anchor='center')

    label_longitude = tk.Label(window, text='Longitude', font=('Arial', 24, 'bold'))
    label_longitude.place(x=WIDTH/4, y=385, anchor='center')

    textbox_longitude = tk.Entry(width=10)
    textbox_longitude.place(x=WIDTH/2, y=385, anchor='center')

    label_latitude = tk.Label(window, text='Latitude', font=('Arial', 24, 'bold'))
    label_latitude.place(x=WIDTH/4, y=420, anchor='center')

    textbox_latitude = tk.Entry(width=10)
    textbox_latitude.place(x=WIDTH/2, y=420, anchor='center')

    #Submission button widget
    button = tk.Button(text='Submit details', command=button_clicked)
    button.place(x=WIDTH/2, y=500, anchor='center')





def show_message(message):

    # Remove existing widgets
    for widget in window.winfo_children():
        widget.destroy()

    # Display error message and 'go back' button to return to the main screen
    message_label = tk.Label(window, text=message, font=('Arial', 24, 'bold'), fg='black')
    message_label.config(wraplength=window.winfo_width())
    message_label.place(x=WIDTH/2, y=100, anchor='center')

    go_back_button = tk.Button(text='Go Back', command=setup_main_ui)
    go_back_button.place(x=WIDTH/2, y=500, anchor='center')






def button_clicked():

    # Obtain the email address, longitude and latitude inputs
    email_address = textbox_email.get()
    longitude = textbox_longitude.get()
    latitude = textbox_latitude.get()

    # Raise error when email address left blank or latitude and longitude inputs being invalid values
    try:
        email_address = validate_email(email_address)
        lat, lon = validate_coordinates(latitude, longitude)
    except ValueError as error_message:
        show_message(str(error_message))
        return

    # Check if email address already exists in the registry, and update coordinates if so
    # If not in the registry, add email address to registry with the input coordinates
    if email_address in registrations:
        registered_lat, registered_long = registrations[email_address]
        if (latitude == registered_lat) and (longitude == registered_long):
            message = 'The details entered already exist in our system. Try again with new details or keep an eye out for our ISS notifications!'
        else:
            registrations[email_address] = [latitude, longitude]
            message = f'Your coordinates have been updated. You will be notified at {email_address} each time the ISS is within 5 degrees of distance from your new location!'
    else:
        registrations[email_address] = [latitude, longitude]
        message = f'Thank you! You will be notified at {email_address} each time the ISS is within 5 degrees of distance from you!'

    with open('Registrations.py', 'w') as f:
        f.write(f"registrations = {registrations}\n")

    # If not already started, starts thread to run the check_iss_and_notify function in the background whilst the app is open.
    # Thus we ensure that check_iss_and_notify runs in a single thread regardless of how many times the button has been clicked
    # Note that for practicality reasons this thread was set up as a daemon thread, as the check_iss_and_notify
    # function is an infinite loop that will make the thread run indefinitely if daemon = False, preventing us from
    # closing the app unless we forcefully stop the programme from running in the terminal.

    if not iss_thread_started:
        threading.Thread(target=check_iss_and_notify, daemon=True).start()
        iss_thread_started = True

    show_message(message)

    # The functionality of this app would be optimised if this code ran in the cloud, where check_iss_and_notify would
    # run continuously and check the ISS position every 10 seconds as defined. Incorporating this code into the cloud
    # goes beyond the scope of this project





# Displays main screen widgets
setup_main_ui()




# window.mainloop() in tkinter runs an infinite loop which keeps the window open until manually closed by the user and keeps
# the app responsive to events like button clicks or keyboard inputs
window.mainloop()
