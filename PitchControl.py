import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username and password are correct
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        open_main_gui()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_main_gui():
    # Create a new window for the main GUI
    main_gui = tk.Toplevel(root)
    main_gui.title("Main GUI")

    # The Screen Pixel Quality (width x height) = 1463 x 914
    screen_width = root.winfo_screenwidth() #stores the width of the computer running
    screen_height = root.winfo_screenheight() #stores the height of the computer running

    # ------------- STYLING --------------
    s = ttk.Style()
    s.configure('userFrame.TFrame', background = '#EDEAE4', relief = 'sunken')
    s.configure('angularVelocityFrame.TFrame', background ='#F9F8F7', relief = 'sunken')
    s.configure('animationFrame.TFrame', background = '#F9F8F7', relief = 'sunken')
    s.configure('graphFrame.TFrame', background ='#F9F8F7', relief = 'sunken')
    s.configure('serialMonitorFrame.TFrame', background ='#F9F8F7', relief = 'sunken')
    s.configure('yieldAngleFrame.TFrame',background='#F9F8F7',relief= 'sunken')


    # Create and configure frames as per your styling
    userFrame = ttk.Frame(main_gui, width=300, height=914, style='userFrame.TFrame')
    userFrame.grid(row=0, column=0, rowspan=2, sticky='NSWE')

    angularVelocityFrame = ttk.Frame(main_gui, width=500, height=447, style='angularVelocityFrame.TFrame')
    angularVelocityFrame.grid(row=0, column=1, sticky='NSEW')

    animationFrame = ttk.Frame(main_gui, width=500, height=447, style='animationFrame.TFrame')
    animationFrame.grid(row=0, column=2, sticky='NSWE')

    graphFrame = ttk.Frame(main_gui, width=500, height=447, style='graphFrame.TFrame')
    graphFrame.grid(row=1, column=2, sticky='NSEW')

    yieldAngleFrame = ttk.Frame(main_gui, width=500, height=447, style='yieldAngleFrame.TFrame')
    yieldAngleFrame.grid(row=1, column=1, sticky='NSEW')

    main_gui.columnconfigure(0, weight=1)
    main_gui.columnconfigure(1, weight=1)
    main_gui.columnconfigure(2, weight=1)
    main_gui.rowconfigure(0, weight=1)
    main_gui.rowconfigure(1, weight=1)

# Create main window
root = tk.Tk()
root.title("Login")

# Username Label and Entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.E)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=20, pady=5)

# Password Label and Entry
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=20, pady=20, sticky=tk.E)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=20, pady=5)

# Login Button
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the main event loop
root.mainloop()
