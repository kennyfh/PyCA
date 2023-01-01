import tkinter as tk

# Create the main window
root = tk.Tk()

# Create a label widget with a large font to use as the header
header_label = tk.Label(root, text="This is the header", font=("Helvetica", 24))

# Add padding above and below the header and center it within the available space
header_label.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

# Run the main loop
root.mainloop()
