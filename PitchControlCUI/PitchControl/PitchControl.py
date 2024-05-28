import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
import time
import threading
import random

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    # For demonstration, we'll just show a message box
    # In a real application, you'd validate the username and password here
    if username == "admin" and password == "1234":
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        login_window.destroy()
        create_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def create_main_window():
    # Create the main window
    root = tk.Tk()
    root.title("Pitch Control")

    # Ensure the window resizes properly with the content
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # -------------------- STYLING AND IMAGES -------------------- #
    s = ttk.Style()
    s.configure('MainFrame.TFrame', background="white")
    s.configure('UserFrame.TFrame', background="#27559C")
    s.configure("AngularVelocityFrame.TFrame", background="white")
    s.configure("AnimationFrame.TFrame", background="white")
    s.configure("SerialMonitorFrame.TFrame", background="white")
    s.configure("FunctionsFrame.TFrame", background="#27559c")
    s.configure("UserFrameLabel.TLabel",
                background="#387adf",
                font=('Montserrat', 13),
                foreground='white',
                padding=(5, 5, 5, 5),
                width=18
                )
    s.configure("DateAndTimeLabel.TLabel",
                background="#387adf",
                font=('Montserrat', 13),
                foreground='white',
                padding=(5, 5, 5, 5),
                width=18
                )

    colour1 = "white"
    colour2 = "#05d7ff"
    colour3 = "#65e7ff"
    colour4 = "white"

    # region Images
    LogoImageObject = Image.open("images/logo_image.png").resize((200, 200))
    LogoImage = ImageTk.PhotoImage(LogoImageObject)

    ParametersImageObject = Image.open("images/counters.png").resize((1000, 300))
    ParametersImage = ImageTk.PhotoImage(ParametersImageObject)

    # -------------------- WIDGETS & FRAMES CONFIGURATION -------------------- #

    # The Screen Pixel Quality (width x height) = 1460 x 914
    MainFrame = ttk.Frame(root, width=1460, height=914, style='MainFrame.TFrame')
    MainFrame.grid(sticky="NSEW")

    UserFrame = ttk.Frame(MainFrame, width=250, height=914, style='UserFrame.TFrame')
    UserFrame.grid(row=0, column=0, rowspan=2, sticky='NSEW')

    AngularVelocityFrame = ttk.Frame(MainFrame, width=505, height=357, style='AngularVelocityFrame.TFrame')
    AngularVelocityFrame.grid(row=0, column=1, sticky='NSEW')

    AnimationFrame = ttk.Frame(MainFrame, width=505, height=357, style='AnimationFrame.TFrame')
    AnimationFrame.grid(row=0, column=2, sticky='NSEW')

    SerialMonitorFrame = ttk.Frame(MainFrame, width=1010, height=200, style='SerialMonitorFrame.TFrame')
    SerialMonitorFrame.grid(row=1, column=1, columnspan=2, sticky='NSEW')

    FunctionsFrame = ttk.Frame(MainFrame, width=200, height=914, style='FunctionsFrame.TFrame')
    FunctionsFrame.grid(row=0, column=3, rowspan=2, sticky='NSEW')

    # UserFrame Section
    LogoLabel = ttk.Label(UserFrame, image=LogoImage, background="#27559C")
    LogoLabel.grid(row=0, column=0, sticky='NEW')
    LogoLabel.configure(anchor="center")

    ParameterLabel = ttk.Label(SerialMonitorFrame, image=ParametersImage, background="white")
    ParameterLabel.grid(row = 2, column = 0, sticky = 'SEW')
    ParameterLabel.configure(text= "\n\n\n\n", anchor="center")

    # -------------------- GRID CONFIGURATION -------------------- #
    # Configure rows and columns for MainFrame
    MainFrame.rowconfigure(0, weight=1)
    MainFrame.rowconfigure(1, weight=1)
    MainFrame.columnconfigure(0, weight=1)
    MainFrame.columnconfigure(1, weight=1)
    MainFrame.columnconfigure(2, weight=1)
    MainFrame.columnconfigure(3, weight=1)

    UserFrame.rowconfigure(0, weight=1)
    UserFrame.rowconfigure(1, weight=1)
    UserFrame.rowconfigure(2, weight=1)
    UserFrame.columnconfigure(0, weight=1)

    AngularVelocityFrame.rowconfigure(0, weight=1)
    AngularVelocityFrame.columnconfigure(0, weight=1)

    AnimationFrame.rowconfigure(0, weight=1)
    AnimationFrame.columnconfigure(0, weight=1)

    FunctionsFrame.rowconfigure(0, weight=1)
    FunctionsFrame.rowconfigure(1, weight=1)
    FunctionsFrame.rowconfigure(2, weight=1)
    FunctionsFrame.rowconfigure(3, weight=1)
    FunctionsFrame.columnconfigure(0, weight=1)

    AngularVelocityFrame.rowconfigure(0, weight=1)
    AngularVelocityFrame.rowconfigure(1, weight=1)
    AngularVelocityFrame.columnconfigure(0, weight=1)



    # Ensure the MainFrame fills the root window
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # UserFrameLabel
    UserFrameLabel = ttk.Label(UserFrame, text=
                               "Name: Admin\n"
                               "Engineer's ID: A123456\n"
                               "Occupation: Engineer\n"
                               "Turbine Unit: X257\n\n"
                               "Date: 21/04/2024\n"
                               "Time: 15:58 p.m.\n"
                               "Region: Thessaloniki",
                               style = "UserFrameLabel.TLabel"
                               )
    UserFrameLabel.grid(row=1, column=0, sticky='NWE')
    UserFrameLabel.configure(
       anchor="center",
       font=("Montserrat", 13)
    )

    # Create and display the figure in AngularVelocityFrame
    figureRPM = Figure(figsize=(6, 5), dpi=80)
    ax = figureRPM.add_subplot(111)
    x_data, y_data = [], []

    def update_plot():
        x_data.append(time.time())
        y_data.append(random.randint(38, 45))  # Να τεστάρουμε εδώ να βάλουμε στη θέση y_data = rpm
        if len(x_data) > 100:  # Limit to the latest 20 data points
            x_data.pop(0)
            y_data.pop(0)
        ax.clear()
        # ax.x_label("Time(sec)", font=("Montserrat", 10))
        # ax.y_label("Angular Velocity(rpm)", font=("Montserrat", 10))
        # ax.title("Angular Velocity", loc='center', font=("Montserrat", 10))
        ax.plot(x_data, y_data)  # Να τεστάρουμε εδώ να βάλουμε στη θέση y_data = rpm
        canvas.draw()
        root.after(500, update_plot)  # Update every second

    canvas = FigureCanvasTkAgg(figureRPM, master=AngularVelocityFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky='NSEW')

    # update_plot()  # Start the update loop


    # GIF Implementation
    # Load the GIF image
    gif_image = tk.PhotoImage(file="images/wind_turbine_gif.gif")

    # Create a label to display the GIF image
    gif_label = ttk.Label(AnimationFrame, image=gif_image)
    gif_label.grid(row=0, column=0, sticky="NSE")

    # Create a canvas for the Matplotlib figure
    canvas.get_tk_widget().grid(row=0, column=0, sticky='NSE')

    # Function to update the GIF image periodically (for demonstration)
    """def update_gif():
        # Load the GIF image again to simulate dynamic changes
        updated_gif_image = Image.open("images/wind_turbine_gif.gif").resize((200, 200))
        gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(updated_gif_image)]

        # Update the GIF label with the new frames
        gif_label.config(image=gif_frames[0])

        # Schedule the function to update the next frame after a delay
        def update_frame(index):
            gif_label.config(image=gif_frames[index])
            # Increment the index and wrap around if necessary
            index = (index + 1) % len(gif_frames)
            # Call update_frame again after a delay to create animation effect
            root.after(100, update_frame, index)

        # Start the animation by updating the frames
        update_frame(0)

    # Call the function to start updating the GIF image
    update_gif()"""

    # Buttons
    LogoutButton = tk.Button(
        UserFrame,
        background=colour1,
        foreground=colour2,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='white',
        width=10,
        height=2,
        cursor='hand2',
        border=5,
        text='Logout',
        font=("Montserrat", 16, "bold")
    )

    LogoutButton.grid(row=3, column=0, sticky = "NWE")

    # Buttons Configuration
    # Add buttons to FunctionsFrame

    button1 = tk.Button(
        FunctionsFrame,
        background=colour1,
        foreground=colour2,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='white',
        width=13,
        height=4,
        cursor='hand2',
        border=5,
        text='ON/OFF',
        font=("Montserrat", 16, "bold")
    )

    button1.grid(row=0, column=0, sticky = "NSEW")

    button2 = tk.Button(
        FunctionsFrame,
        background=colour1,
        foreground=colour2,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='white',
        width=13,
        height=4,
        cursor='hand2',
        border=5,
        text='Auto Check',
        font=("Montserrat", 16, "bold")
    )
    button2.grid(row=1, column=0, sticky = "NSEW")

    button3 = tk.Button(
        FunctionsFrame,
        background=colour1,
        foreground=colour2,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='white',
        width=13,
        height=4,
        cursor='hand2',
        border=5,
        text='Repair Mode',
        font=("Montserrat", 16, "bold")
    )
    button3.grid(row=2, column=0, sticky = "NSEW")

    button4 = tk.Button(
        FunctionsFrame,
        background=colour1,
        foreground=colour2,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='white',
        width=13,
        height=4,
        cursor='hand2',
        border=5,
        text='Live Feed',
        font=("Montserrat", 16, "bold")
    )
    button4.grid(row=3, column=0, sticky = "NSEW")

    button5 = tk.Button(
        FunctionsFrame,
        background="red",
        foreground="white",
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='white',
        width=13,
        height=4,
        cursor='hand2',
        border=5,
        text='Emergency Stop',
        font=("Montserrat", 16, "bold")
    )
    button5.grid(row=4, column=0, sticky = "NSEW")


    root.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

# Create a frame for the login form
login_frame = ttk.Frame(login_window, padding="20")
login_frame.grid(row=0, column=0, sticky="NSEW")

# Configure the grid
login_window.columnconfigure(0, weight=1)
login_window.rowconfigure(0, weight=1)
login_frame.columnconfigure(0, weight=1)
login_frame.columnconfigure(1, weight=1)

# Username label and entry
username_label = ttk.Label(login_frame, text="Username:")
username_label.grid(row=0, column=0, sticky="W", pady=5)
username_entry = ttk.Entry(login_frame)
username_entry.grid(row=0, column=1, sticky="EW", pady=5)

# Password label and entry
password_label = ttk.Label(login_frame, text="Password:")
password_label.grid(row=1, column=0, sticky="W", pady=5)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, sticky="EW", pady=5)

login_button = ttk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)


# Make the login frame fill the window
login_frame.grid_columnconfigure(0, weight=1)
login_frame.grid_columnconfigure(1, weight=1)


# Run the login window
login_window.mainloop()
