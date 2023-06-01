import tkinter as tk
import datetime
import paho.mqtt.client as mqtt
import gpiod
import time

# Set up the MQTT client
broker_address = "localhost"
MQTT_PORT = 1883
topic = "counter"
client = mqtt.Client()
counter = 0

# Open the GPIO chip and lines
chip = gpiod.Chip('gpiochip1')
input_line = chip.get_line(92) # input line
output_line = chip.get_line(91) # output line

# Request the GPIO lines
input_line.request(consumer='my_gpio_script', type=gpiod.LINE_REQ_DIR_IN)
output_line.request(consumer='my_gpio_script', type=gpiod.LINE_REQ_DIR_OUT)

# Callback function for when a message is received on the counter topic
def on_message(client, userdata, message):
    global counter
    counter = int(message.payload.decode())

# Connect to the MQTT broker and subscribe to the counter topic
client.connect(broker_address)
client.subscribe(topic)
client.on_message = on_message

# create a Tkinter window
root = tk.Tk()

# set the window size
root.geometry("800x600")

# set the background image
bg_image = tk.PhotoImage(file="trash.PNG")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

# make the window fullscreen
root.attributes("-fullscreen", True)

# create a label with the text
counterbox = tk.Label(root, text="0", font=("Arial", 72), fg="Black", bg="white", highlightthickness=0, highlightbackground="white")

# set the position of the label
counterbox.place(relx=0.5, rely=0.5, anchor='center', y=-100, x=-50)

# bind the Escape key to exit fullscreen mode
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# function to update the label and check for MQTT messages
def update_label():
    global counter, bg_label, bg_image, counterbox

    # Check for MQTT messages
    client.loop()

    # Check for input from the sensor
    input_value = input_line.get_value()
    if input_value == 0:
        print("Trash thrown in")
        client.publish(topic, counter+1)

        # change the background image to trashd.PNG
        bg_image = tk.PhotoImage(file="trashd.PNG")
        bg_label.config(image=bg_image)  # update the image of the bg_label widget

        # hide the counter label
        counterbox.place_forget()

        # schedule the function to update the background image and counter label after 2 seconds
        root.after(1, show_bg_and_counter)
    else:
        client.loop()
        counterbox.config(text=str(counter))        
    # schedule the function to run again in 100ms
    root.after(100, update_label)

# function to show the background image and counter label after 2 seconds
def show_bg_and_counter():
    global bg_label, bg_image, counterbox
    time.sleep(2)
    # change the background image to trash.PNG
    bg_image = tk.PhotoImage(file="trash.PNG")
    bg_label.config(image=bg_image)  # update the image of the bg_label widget

    # show the counter label
    counterbox.config(text=str(counter)) # update the counter text
    counterbox.place(relx=0.5, rely=0.5, anchor='center', y=-100, x=-50)

# schedule the initial call to the update_label function
root.after(100, update_label)

# run the window loop
root.mainloop()

# Release the GPIO lines and chip
input_line.release()
output_line.release()
chip.close()

# Disconnect from the MQTT broker
client.disconnect()



