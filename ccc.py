import tkinter as tk

# Create the main window
window = tk.Tk()

# Create a frame to hold the Text widget and the Scrollbar widget
frame = tk.Frame(window)
frame.pack()

# Create a Text widget to display the log
log_text = tk.Text(frame)
log_text.pack(side=tk.LEFT)

# Create a Scrollbar widget and link it to the Text widget
scrollbar = tk.Scrollbar(frame, command=log_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.configure(yscrollcommand=scrollbar.set)

# Function to append a message to the log
def log(message):
    for i in range(3):
        log_text.insert(tk.END, message + "\n")

# Test the log function
log("This is a test message.")

# Run the Tkinter event loop
window.mainloop()
