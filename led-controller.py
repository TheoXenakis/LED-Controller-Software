"****************************************************************************"
"*    CREATED BY THEO XENAKIS - Free to use for Prizmatix LED-Ctrl users    *"
"****************************************************************************"
#IMPORT PACKAGES
import tkinter as tk #built-in package, no extra installation needed
from tkinter import messagebox
import serial #pip install pyserial 

"+---------------------------- led-controller.py ---------------------------+"
def test_connection():
    com_port = com_port_entry.get().strip() #get the COM port from the entry field, remove extra spaces
    try:
        #try to open the serial conenction
        ser = serial.Serial(port=com_port, baudrate=9600, timeout=1) #change speed if expecting 57600 baud
        ser.close() #immediately close the connection after the test
        messagebox.showinfo("Connection Test", f"Successfully connected to {com_port}")
    except Exception as e:
        messagebox.showerror("Connection Test", f"Failed to connect to {com_port}\nError: {e}")

#Create the main window
root = tk.Tk()
root.title("Prizmatix LED Controller")
root.geometry("300x150")

#Create the label and entry for COM port
com_port_label = tk.Label(root, text="Enter COM Port (e.g., COM3):")
com_port_label.pack(pady=10) #pads 10 pixels vertically

com_entry = tk.Entry(root, width=20) #text field where the user can enter the COM port - width of 20 characters
com_entry.pack(pady=5) #pads 5 pixels vertically 

#Button to test the connection
test_button = tk.Button(root, text="Test Connection", command=test_connection)
test_button.pack(pady=20) #pads 20 pixels vertically

root.mainloop() #start the GUI event loop