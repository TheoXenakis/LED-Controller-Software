"****************************************************************************"
"*    CREATED BY THEO XENAKIS - Free to use for Prizmatix LED-Ctrl users    *"
"****************************************************************************"
#IMPORT PACKAGES
import tkinter as tk #built-in package, no extra installation needed
from tkinter import messagebox
import serial #pip install pyserial 
import serial.tools.list_ports
import time
import threading

cancel_flag = threading.Event()

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
        ser.write(b'H')  # OPTION 1: Send 'ON' command to the device via 'H' command
        #ser.write(b'ON) # OPTION 2: Send 'ON' command to the device via 'ON' command (UNCOMMENT IF NEEDED)
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
        ser.write(b'L')  # OPTION 1: Send 'OFF' command to the device via the 'L' command
        #ser.write(b'OFF) # OPTION 1: Send 'OFF' command to the device via 'OFF' command (UNCOMMENT IF NEEDED)
        ser.close()
        print("LED turned OFF")
        messagebox.showinfo("Success", "LED turned OFF")
    except Exception as e:
        print(f"ERROR - Could not send OFF command: {e}")
        messagebox.showerror("Error", f"Failed to turn OFF LED\n\n{e}")

def start_timer():
    def run_timer():
        cancel_flag.clear()
        try:
            hours = int(hours_val.get())
            minutes = int(minutes_val.get())
            seconds = int(seconds_val.get())
            interval = (hours * 3600) + (minutes * 60) + seconds
            cycles = int(cycles_val.get())
            if interval <= 0 or cycles <= 0:
                raise ValueError
        except ValueError:
            root.after(0, lambda:messagebox.showerror("Error", "Please enter a valid number for the timer."))
            return

        com_port = selected_port.get()
        try:
            ser = serial.Serial(port=com_port, baudrate=9600, timeout=1)
            for cycle in range(cycles):
                if cancel_flag.is_set():
                    print("Timer cancelled.")
                    ser.close()
                    root.after(0, lambda: messagebox.showinfo("Timer", "Timer cancelled."))
                    return

                ser.write(b'H')
                print(f"Cycle {cycle+1}/{cycles}: LED ON")
                root.after(0, root.update)

                # Sleep in small increments for ON interval
                sleep_time = 0
                while sleep_time < interval:
                    if cancel_flag.is_set():
                        print("Timer cancelled during ON interval.")
                        ser.close()
                        root.after(0, lambda: messagebox.showinfo("Timer", "Timer cancelled."))
                        return
                    time.sleep(0.1)
                    sleep_time += 0.1

                if cancel_flag.is_set():
                    print("Timer cancelled.")
                    ser.close()
                    root.after(0, lambda: messagebox.showinfo("Timer", "Timer cancelled."))
                    return

                ser.write(b'L')
                print(f"Cycle {cycle+1}/{cycles}: LED OFF")
                root.update()

                # Sleep in small increments for OFF interval (except after last cycle)
                if cycle < cycles - 1:
                    sleep_time = 0
                    while sleep_time < interval:
                        if cancel_flag.is_set():
                            print("Timer cancelled during OFF interval.")
                            ser.close()
                            root.after(0, lambda: messagebox.showinfo("Timer", "Timer cancelled."))
                            return
                        time.sleep(0.1)
                        sleep_time += 0.1

            ser.close()
            root.after(0, lambda: messagebox.showinfo("Timer", f"Completed {cycles} ON/OFF cycles at {interval}s each."))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Error", f"Timer failed\n\n{e}"))

    threading.Thread(target=run_timer, daemon=True).start()

def cancel_timer():
    cancel_flag.set()


"+------------------ GUI SETUP ------------------+"
#Create the main window
root = tk.Tk()
root.title("Prizmatix LED Controller")
root.geometry("450x300") #width x height

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

#Interval Dropdowns
interval_frame = tk.Frame(root)
interval_frame.pack()

interval_label = tk.Label(interval_frame, text="Run For:")
interval_label.grid(row=0, column=0, padx=5)

#sub-dropdowns for hours, minutes, seconds
hours_val = tk.StringVar(value="0")
minutes_val = tk.StringVar(value="0")
seconds_val = tk.StringVar(value="1")

hours_menu = tk.OptionMenu(interval_frame, hours_val, *[str(i) for i in range(0, 24)])
hours_menu.grid(row=0, column=1)
tk.Label(interval_frame, text="h").grid(row=0, column=2)

minutes_menu = tk.OptionMenu(interval_frame, minutes_val, *[str(i) for i in range(0, 60)])
minutes_menu.grid(row=0, column=3)
tk.Label(interval_frame, text="m").grid(row=0, column=4)

seconds_menu = tk.OptionMenu(interval_frame, seconds_val, *[str(i) for i in range(0, 60)])
seconds_menu.grid(row=0, column=5)
tk.Label(interval_frame, text="s").grid(row=0, column=6)

#Cycles Dropdown
cycles_label = tk.Label(root, text="Number of Cycles to Run:")
cycles_label.pack()
cycles_val = tk.StringVar(value="1")
cycles_menu = tk.OptionMenu(root, cycles_val, *[str(i) for i in range(1, 101)])
cycles_menu.pack()

#Button to start the timer
timer_button = tk.Button(root, text="Start Timer", command=start_timer)
timer_button.pack(pady=5)

#Button to cancel the timer
cancel_button = tk.Button(root, text="Cancel Timer", command=cancel_timer)
cancel_button.pack(pady=5)

root.mainloop() #start the GUI event loop