"****************************************************************************"
"*    CREATED BY THEO XENAKIS - Free to use for Prizmatix LED-Ctrl users    *"
"****************************************************************************"
#IMPORT PACKAGES
import tkinter as tk #built-in package, no extra installation needed
from tkinter import messagebox
import serial #pip install pyserial 
import serial.tools.list_ports

"****************************************************************************"
"+---------------------------- led-controller.py ---------------------------+"
"****************************************************************************"

"+---------- Testing Communication and Port Management ----------+"

def test_connection():
    com_port = selected_port.get()
    print(f"Testing connection to {com_port}...")  # debug print

    try:
        ser = serial.Serial(port=com_port, baudrate=9600, timeout=1)
        ser.close()
        print("SUCCESS - Serial opened and closed")
        messagebox.showinfo("Success", f"Connected successfully to {com_port}")
    except Exception as e:
        print(f"ERROR - Could not open {com_port}: {e}")
        messagebox.showerror("Error", f"Failed to connect to {com_port}\n\n{e}")

def get_available_ports():
    ports = serial.tools.list_ports.comports() #retrieve a list of available serial ports (in DEVICE MANAGER)
    return [port.device for port in ports]

def refresh_ports():
    available_ports = get_available_ports()
    menu = com_dropdown["menu"]
    menu.delete(0, "end") # clear existing options

    # repopulate the menu with updated ports
    if available_ports:
        for port in available_ports:
            menu.add_command(label=port, command=lambda value=port: selected_port.set(value))
        selected_port.set(available_ports[0]) #default to the first available 
        print("Ports refreshed.")
    else:
        selected_port.set("No Ports Found")
        messagebox.showwarning("Warning", "No COM ports found. Please connect your device.")
        print("WARNING - No COM ports found. Please connect your device.")

"+---------- LED Control Functions ----------+"

def turn_on():
    com_port = selected_port.get()
    try:
        ser = serial.Serial(port=com_port, baudrate=9600, timeout=1)
        ser.write(b'H')  # Send 'ON' command to the device
        ser.close()
        print("LED turned ON")
        messagebox.showinfo("Success", "LED turned ON")
    except Exception as e:
        print(f"ERROR - Could not send ON command: {e}")
        messagebox.showerror("Error", f"Failed to turn ON LED\n\n{e}")

def turn_off():
    com_port = selected_port.get()
    try:
        ser = serial.Serial(port=com_port, baudrate=9600, timeout=1)
        ser.write(b'L')  # Send 'OFF' command to the device
        ser.close()
        print("LED turned OFF")
        messagebox.showinfo("Success", "LED turned OFF")
    except Exception as e:
        print(f"ERROR - Could not send OFF command: {e}")
        messagebox.showerror("Error", f"Failed to turn OFF LED\n\n{e}")

"+------------------ GUI SETUP ------------------+"
#Create the main window
root = tk.Tk()
root.title("Prizmatix LED Controller")
root.geometry("300x150")

#Create the label and entry for COM port
com_port_label = tk.Label(root, text="Select COM Port:")
selected_port = tk.StringVar(root) #creates a string variable to hold the selected port

available_ports = get_available_ports()
if available_ports:
    selected_port.set(available_ports[0]) #set the default value to the first available port
else:
    selected_port.set("No Ports Found")
    messagebox.showwarning("Warning", "No COM ports found. Please connect your device.")
    print("WARNING - No COM ports found. Please connect your device.")

#Create dropdown menu for available COM ports
com_dropdown = tk.OptionMenu(root, selected_port, *available_ports)
com_dropdown.pack(pady=5) #pads 5 pixels vertically

#Button to test the connection
test_button = tk.Button(root, text="Test Connection", command=test_connection)
test_button.pack(pady=20) #pads 20 pixels vertically

#Button to refresh the list of COM ports
refresh_button = tk.Button(root, text="Refresh Ports", command=refresh_ports)
refresh_button.pack(pady=5) #pads 5 pixels vertically

#Button to turn LED ON
on_button = tk.Button(root, text="Turn LED ON", command=turn_on)
on_button.pack(pady=5) #pads 5 pixels vertically

#Button to turn LED OFF
off_button = tk.Button(root, text="Turn LED OFF", command=turn_off)
off_button.pack(pady=5) #pads 5 pixels vertically

root.mainloop() #start the GUI event loop